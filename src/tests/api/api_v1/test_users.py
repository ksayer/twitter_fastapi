import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings

pytestmark = pytest.mark.asyncio


async def test_get_users_endpoint(client: AsyncClient, db: AsyncSession):
    response = await client.get(f'{settings.API_PREFIX_V1}/users')
    assert response.json() == [{'name': 'Fix', 'key': 'test11', 'id': 1}]
