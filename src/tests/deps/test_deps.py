import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps
from src.api.deps import get_session
from src.core.exceptions import ValidationError

pytestmark = pytest.mark.asyncio


async def test_get_current_user(db: AsyncSession):
    user = await deps.get_current_user(db, api_key='test11')
    assert user.name == 'Fix'
    with pytest.raises(ValidationError):
        await deps.get_current_user(db, api_key='test123')


async def test_get_session():
    async for sess in get_session():
        assert isinstance(sess, AsyncSession)
