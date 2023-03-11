import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.config import settings
from src.tests.factories import TwitFactory

pytestmark = pytest.mark.asyncio


async def test_create_twit(client: AsyncClient, db: AsyncSession, user_api_key: dict):
    twit = TwitFactory.build()
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit.to_json(), headers=user_api_key)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit_with_media(
    client: AsyncClient, db: AsyncSession, user_api_key: dict, twit_with_media
):
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit_with_media, headers=user_api_key)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    assert len(twits[1].media) == 1
    assert len(twits[0].media) == 0


async def test_deleting_twit(client: AsyncClient, db: AsyncSession, user_api_key: dict):
    url = f'{settings.API_PREFIX_V1}/twits/1/'
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    response = await client.delete(url, headers=user_api_key)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 0
    assert response.status_code == 200


async def test_deleting_wrong_twit(
    client: AsyncClient, db: AsyncSession, user_api_key: dict
):
    headers = {'api-key': 'test22222'}
    url = f'{settings.API_PREFIX_V1}/twits/1/'
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    response = await client.delete(url, headers=headers)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    assert response.status_code == 404


async def test_api_setting_like(
    client: AsyncClient, db: AsyncSession, user_api_key: dict
):
    twit = await TwitFactory.create()
    url = f'{settings.API_PREFIX_V1}/twits/{twit.tweet_id}/likes/'
    response = await client.post(url, headers=user_api_key)
    assert response.status_code == 200
    twit = await crud.twit.get(db, tweet_id=twit.tweet_id)
    assert len(twit.likes) == 1
