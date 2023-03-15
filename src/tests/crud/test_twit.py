import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.tests.factories import FollowFactory, LikeFactory, TwitFactory, UserFactory

pytestmark = pytest.mark.asyncio


async def test_fixture(db: AsyncSession):
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1


async def test_get_twits(db: AsyncSession):
    twit = TwitFactory.build()
    db.add(twit)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit(db: AsyncSession):
    twit = TwitFactory.build()
    obj_in = twit.to_json()
    obj_in.pop('user_id')
    user = await UserFactory.create()
    await crud.twit.create_with_user(db, obj_in=obj_in, user_id=user.id)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit_with_media(db: AsyncSession, twit_with_media):
    user = await UserFactory.create()
    tweet = await crud.twit.create_with_user(
        db, obj_in=twit_with_media, user_id=user.id
    )
    twits = await crud.twit.get_multi(db)
    assert len(tweet.media) == 1
    assert len(twits) == 2


async def test_deleting_twit(db: AsyncSession, twit_with_media):
    user = await UserFactory.create()
    tweet = await crud.twit.create_with_user(
        db, obj_in=twit_with_media, user_id=user.id
    )
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    await crud.twit.delete_users_tweet(db, twit_id=tweet.tweet_id, user_id=user.id)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1


async def test_deleting_twit_with_wrong_user(db: AsyncSession, twit_with_media):
    user = await UserFactory.create()
    tweet = await crud.twit.create_with_user(
        db, obj_in=twit_with_media, user_id=user.id
    )
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    with pytest.raises(HTTPException):
        await crud.twit.delete_users_tweet(
            db, twit_id=tweet.tweet_id, user_id=user.id + 1
        )
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_crud_setting_like(db: AsyncSession):
    twit = await TwitFactory.create()
    user = await UserFactory.create()
    await crud.twit.set_like(db, user_id=user.id, twit_id=twit.tweet_id)
    twit = await crud.twit.get(db, tweet_id=twit.tweet_id)
    assert len(twit.liked_users) == 1
    assert twit.liked_users[0].id == user.id


async def test_crud_deleting_like(db: AsyncSession):
    like = await LikeFactory.create()
    await crud.twit.delete_like(db, twit_id=like.twit_id, user_id=like.user_id)
    with pytest.raises(HTTPException):
        await crud.like.get(db, twit_id=like.twit_id, user_id=like.user_id)


async def test_crud_deleting_alien_like(db: AsyncSession):
    like = await LikeFactory.create()
    user = await UserFactory.create()
    with pytest.raises(HTTPException):
        await crud.twit.delete_like(db, twit_id=like.twit_id, user_id=user.id)


async def test_crud_get_users_twit(db: AsyncSession):
    user_1 = await UserFactory.create()
    user_2 = await UserFactory.create()
    user_3 = await UserFactory.create()
    await TwitFactory.create(user=user_1)
    await TwitFactory.create(user=user_1)
    await TwitFactory.create(user=user_2)
    await TwitFactory.create(user=user_3)
    await FollowFactory.create(follower=user_2, following=user_1)
    await FollowFactory.create(follower=user_1, following=user_2)
    await FollowFactory.create(follower=user_3, following=user_2)
    twits_user_2 = await crud.twit.get_users_twits(db, user_id=user_2.id)
    twits_user_1 = await crud.twit.get_users_twits(db, user_id=user_1.id)
    assert len(twits_user_2) == 2
    assert len(twits_user_1) == 1
