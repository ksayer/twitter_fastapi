import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_create_twit(client: AsyncClient, db: AsyncSession):
    twit_data = {'content': 'twitcontent'}
    headers = {'api-key': 'test11'}
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit_data, headers=headers)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
