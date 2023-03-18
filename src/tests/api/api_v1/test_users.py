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
    assert response.status_code == 422


async def test_api_delete_follow_user(client: AsyncClient, db: AsyncSession):
    follow = await FollowFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/{follow.following.id}/follow/'
    response = await client.delete(url, headers={'api-key': follow.follower.key})
    assert response.status_code == 200
    response = await client.delete(url, headers={'api-key': follow.follower.key})
    assert response.status_code == 422


async def test_get_user_info_empty(client: AsyncClient, db: AsyncSession):
    user = await UserFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/me'
    response = await client.get(url, headers={'api-key': user.key})
    assert response.status_code == 200
    json = {
        'result': True,
        'user': {
            'name': user.name,
            'id': user.id,
            'followers': [],
            'following': [],
        },
    }
    assert response.json() == json


async def test_get_my_info(client: AsyncClient, db: AsyncSession, user_info):
    user, follower, following, following_2, json_response = user_info
    url = f'{settings.API_PREFIX_V1}/users/me'
    response = await client.get(url, headers={'api-key': user.key})
    assert response.status_code == 200
    assert response.json() == json_response


async def test_any_user_info(client: AsyncClient, db: AsyncSession, user_info):
    user, follower, following, following_2, json_response = user_info
    url = f'{settings.API_PREFIX_V1}/users/{user.id}'
    response = await client.get(url, headers={'api-key': user.key})
    assert response.status_code == 200
    assert response.json() == json_response


async def test_authorization(client: AsyncClient, db: AsyncSession):
    url = f'{settings.API_PREFIX_V1}/users/1'
    response = await client.get(url, headers={'api-key': 'asdasdasd'})
    assert response.status_code == 403
