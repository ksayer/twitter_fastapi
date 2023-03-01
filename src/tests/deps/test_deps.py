import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps

pytestmark = pytest.mark.asyncio


async def test_get_current_user(db: AsyncSession):
    user = await deps.get_current_user(db, api_key='test11')
    assert user.name == 'Fix'
