import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.models.user import User

pytestmark = pytest.mark.asyncio


async def test_fixture(db: AsyncSession, create_user):
    users = await crud.user.get_all_users(db)
    assert users[0].name == 'Fix'
    assert len(users) == 1


async def test_get_users_with_adding(db: AsyncSession):
    user = User(name='Bar', key='qweqwe')
    db.add(user)
    users = await crud.user.get_all_users(db)
    assert len(users) == 1
    assert users[0].name == 'Bar'
