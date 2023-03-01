import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.models.user import User

pytestmark = pytest.mark.asyncio


async def test_fixture(db: AsyncSession):
    users = await crud.user.get_multi(db)
    assert len(users) == 1


async def test_get_users_with_adding(db: AsyncSession):
    user = User(name='Bar', key='qweqwe')
    db.add(user)
    users = await crud.user.get_multi(db)
    assert len(users) == 2


async def test_get_user_by_key(db: AsyncSession):
    key = 'mykey'
    user = User(name='Foo', key='mykey')
    db.add(user)
    user = await crud.user.get_by_key(db, key=key)
    assert user.key == key
