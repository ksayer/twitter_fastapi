import pytest
from fastapi import UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_create_twit(client: AsyncClient, db: AsyncSession):
    twit_data = {'tweet_data': 'twitcontent'}
    headers = {'api-key': 'test11'}
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit_data, headers=headers)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit_with_media(
    client: AsyncClient, db: AsyncSession, uploaded_file: UploadFile
):
    media = await crud.media.create_and_save_file(db, file=uploaded_file)
    twit_data = {'tweet_data': 'twitcontent', 'tweet_media_ids': [media.id]}
    headers = {'api-key': 'test11'}
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit_data, headers=headers)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    assert len(twits[1].media) == 1
    assert len(twits[0].media) == 0


async def test_deleting_twit(client: AsyncClient, db: AsyncSession):
    headers = {'api-key': 'test11'}
    url = f'{settings.API_PREFIX_V1}/twits/1/'
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    response = await client.delete(url, headers=headers)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 0
    assert response.status_code == 200


async def test_deleting_wrong_twit(client: AsyncClient, db: AsyncSession):
    headers = {'api-key': 'test22222'}
    url = f'{settings.API_PREFIX_V1}/twits/1/'
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    response = await client.delete(url, headers=headers)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    assert response.status_code == 404
