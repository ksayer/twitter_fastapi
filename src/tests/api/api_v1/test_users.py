import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.config import settings
from src.tests.factories import FollowFactory, UserFactory

pytestmark = pytest.mark.asyncio


async def test_api_follow_user(client: AsyncClient, db: AsyncSession):
    follower = await UserFactory.create()
    following = await UserFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/{following.id}/follow/'
    response = await client.post(url, headers={'api-key': follower.key})
    assert response.status_code == 200
    follower = await crud.user.get(db, id=follower.id)
    assert follower.following[0].id == following.id
    response = await client.post(url, headers={'api-key': follower.key})
    assert response.status_code == 400


async def test_api_delete_follow_user(client: AsyncClient, db: AsyncSession):
    follow = await FollowFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/{follow.following.id}/follow/'
    response = await client.delete(url, headers={'api-key': follow.follower.key})
    assert response.status_code == 200
    response = await client.delete(url, headers={'api-key': follow.follower.key})
    assert response.status_code == 400


async def test_get_user_info_empty(client: AsyncClient, db: AsyncSession):
    user = await UserFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/me'
    response = await client.get(url, headers={'api-key': user.key})
    assert response.status_code == 200
    json = {
        'result': True,
        'user': {
            'name': user.name,
            'user_id': user.id,
            'followers': [],
            'following': [],
        },
    }
    assert response.json() == json


async def test_get_user_info(client: AsyncClient, db: AsyncSession):
    user = await UserFactory.create()
    follower = await UserFactory.create()
    following = await UserFactory.create()
    following_2 = await UserFactory.create()
    await crud.follow.follow_user(
        db, follower_user_id=follower.id, following_user_id=user.id
    )
    await crud.follow.follow_user(
        db, follower_user_id=user.id, following_user_id=following.id
    )
    await crud.follow.follow_user(
        db, follower_user_id=user.id, following_user_id=following_2.id
    )
    url = f'{settings.API_PREFIX_V1}/users/me'
    response = await client.get(url, headers={'api-key': user.key})
    assert response.status_code == 200
    json = {
        'result': True,
        'user': {
            'name': user.name,
            'user_id': user.id,
            'followers': [
                {'name': follower.name, 'id': follower.id},
            ],
            'following': [
                {'name': following.name, 'id': following.id},
                {'name': following_2.name, 'id': following_2.id},
            ],
        },
    }
    assert response.json() == json
