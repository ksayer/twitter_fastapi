import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.models.twit import Twit
from src.schemas import TwitIn

pytestmark = pytest.mark.asyncio


async def test_fixture(db: AsyncSession):
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1


async def test_get_twits(db: AsyncSession):
    twit = Twit(tweet_data='another content', user_id=1)
    db.add(twit)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit(db: AsyncSession):
    obj_in = TwitIn(tweet_data='twitcontent')
    await crud.twit.create_with_user(db, obj_in=obj_in, user_id=1)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit_with_media(db: AsyncSession, uploaded_file):
    media = await crud.media.create_and_save_file(db, file=uploaded_file)
    obj_in = TwitIn(tweet_data='twitcontent', tweet_media_ids=[media.id])
    tweet = await crud.twit.create_with_user(db, obj_in=obj_in, user_id=1)
    twits = await crud.twit.get_multi(db)
    assert len(tweet.media) == 1
    assert len(twits) == 2


async def test_deleting_twit(db: AsyncSession, uploaded_file):
    media = await crud.media.create_and_save_file(db, file=uploaded_file)
    obj_in = TwitIn(tweet_data='twitcontent', tweet_media_ids=[media.id])
    tweet = await crud.twit.create_with_user(db, obj_in=obj_in, user_id=1)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    await crud.twit.delete_users_tweet(db, twit_id=tweet.tweet_id, user_id=1)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1


async def test_deleting_twit_with_wrong_user(db: AsyncSession, uploaded_file):
    media = await crud.media.create_and_save_file(db, file=uploaded_file)
    obj_in = TwitIn(tweet_data='twitcontent', tweet_media_ids=[media.id])
    tweet = await crud.twit.create_with_user(db, obj_in=obj_in, user_id=1)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    with pytest.raises(HTTPException):
        await crud.twit.delete_users_tweet(db, twit_id=tweet.tweet_id, user_id=2)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
