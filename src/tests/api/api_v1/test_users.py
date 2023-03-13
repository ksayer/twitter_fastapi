import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.config import settings
from src.tests.factories import FollowFactory, UserFactory

pytestmark = pytest.mark.asyncio


async def test_get_users_endpoint(client: AsyncClient, db: AsyncSession):
    response = await client.get(f'{settings.API_PREFIX_V1}/users')
    assert response.json() == [{'name': 'Fix', 'key': 'test11', 'id': 1}]


async def test_api_follow_user(client: AsyncClient, db: AsyncSession):
    follower = await UserFactory.create()
    following = await UserFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/{following.id}/follow/'
    response = await client.post(url, headers={'api-key': follower.key})
    assert response.status_code == 200
    follower = await crud.user.get(db, id=follower.id)
    assert follower.followings[0].id == following.id
    response = await client.post(url, headers={'api-key': follower.key})
    assert response.status_code == 400


async def test_api_delete_follow_user(client: AsyncClient, db: AsyncSession):
    follow = await FollowFactory.create()
    url = f'{settings.API_PREFIX_V1}/users/{follow.following.id}/follow/'
    response = await client.delete(url, headers={'api-key': follow.follower.key})
    assert response.status_code == 200
    response = await client.delete(url, headers={'api-key': follow.follower.key})
    assert response.status_code == 400
