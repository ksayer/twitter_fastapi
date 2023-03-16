import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.exceptions import ValidationError
from src.tests.factories import FollowFactory, UserFactory

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


async def test_get_user_by_key_exception(db: AsyncSession):
    with pytest.raises(ValidationError):
        await crud.user.get_by_key(db, key='fake-key')


async def test_crud_follow_user(db: AsyncSession):
    follower = await UserFactory.create()
    target_user = await UserFactory.create()
    await crud.follow.follow_user(
        db, follower_user_id=follower.id, following_user_id=target_user.id
    )
    follower = await crud.user.get(db, id=follower.id)
    target_user = await crud.user.get(db, id=target_user.id)
    assert follower.following[0] == target_user
    assert len(follower.followers) == 0
    assert len(target_user.followers) == 1
    with pytest.raises(ValidationError):
        await crud.follow.follow_user(
            db, follower_user_id=follower.id, following_user_id=target_user.id
        )


async def test_crud_follow_wrong_user(db: AsyncSession):
    follower = await UserFactory.create()
    with pytest.raises(ValidationError):
        await crud.follow.follow_user(
            db, follower_user_id=follower.id, following_user_id=follower.id
        )


async def test_crud_delete_follow(db: AsyncSession):
    follow = await FollowFactory.create()
    await crud.follow.delete_follow(
        db, follower_user_id=follow.follower_id, following_user_id=follow.following_id
    )
    with pytest.raises(ValidationError):
        await crud.follow.get(
            db, follower_id=follow.follower_id, following_id=follow.following_id
        )
