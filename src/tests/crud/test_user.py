import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.tests.factories import TwitFactory, UserFactory

pytestmark = pytest.mark.asyncio


async def test_fixture(db: AsyncSession):
    users = await crud.user.get_multi(db)
    assert len(users) == 1


async def test_get_users_with_adding(db: AsyncSession):
    fake_user = UserFactory.build()
    db.add(fake_user)
    users = await crud.user.get_multi(db)
    assert len(users) == 2


async def test_get_user_by_key(db: AsyncSession):
    fake_user = UserFactory.build()
    db.add(fake_user)
    user = await crud.user.get_by_key(db, key=fake_user.key)
    assert user.key == fake_user.key
    # u = await UserFactory.create(db=db)
    t = await TwitFactory.create()
    print(t)
