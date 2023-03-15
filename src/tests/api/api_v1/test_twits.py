import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.config import settings
from src.tests.factories import FollowFactory, LikeFactory, TwitFactory, UserFactory

pytestmark = pytest.mark.asyncio


async def test_create_twit(client: AsyncClient, db: AsyncSession, user_api_key: dict):
    twit = TwitFactory.build()
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit.to_json(), headers=user_api_key)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2


async def test_create_twit_with_media(
    client: AsyncClient, db: AsyncSession, user_api_key: dict, twit_with_media
):
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.post(url, json=twit_with_media, headers=user_api_key)
    assert response.status_code == 201
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
    assert len(twits[1].media) == 1
    assert len(twits[0].media) == 0


async def test_deleting_twit(client: AsyncClient, db: AsyncSession, user_api_key: dict):
    url = f'{settings.API_PREFIX_V1}/twits/1/'
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    response = await client.delete(url, headers=user_api_key)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 0
    assert response.status_code == 200


async def test_deleting_wrong_twit(
    client: AsyncClient, db: AsyncSession, user_api_key: dict
):
    headers = {'api-key': 'test22222'}
    url = f'{settings.API_PREFIX_V1}/twits/1/'
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    response = await client.delete(url, headers=headers)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1
    assert response.status_code == 404


async def test_api_setting_like(
    client: AsyncClient, db: AsyncSession, user_api_key: dict
):
    twit = await TwitFactory.create()
    url = f'{settings.API_PREFIX_V1}/twits/{twit.tweet_id}/likes/'
    response = await client.post(url, headers=user_api_key)
    assert response.status_code == 200
    twit = await crud.twit.get(db, tweet_id=twit.tweet_id)
    assert twit.liked_users[0].key == user_api_key['api-key']
    response = await client.post(url, headers=user_api_key)
    assert response.status_code == 400


async def test_api_deleting_like(client: AsyncClient, db: AsyncSession):
    like = await LikeFactory.create()
    url = f'{settings.API_PREFIX_V1}/twits/{like.twit_id}/likes/'
    response = await client.delete(url, headers={'api-key': like.user.key})
    assert response.status_code == 200


async def test_api_deleting_alien_like(
    client: AsyncClient, db: AsyncSession, user_api_key: dict
):
    like = await LikeFactory.create()
    url = f'{settings.API_PREFIX_V1}/twits/{like.twit_id}/likes/'
    response = await client.delete(url, headers=user_api_key)
    assert response.status_code == 400
    assert response.json() == {"detail": "like not found"}


async def test_get_users_twits(client: AsyncClient, db: AsyncSession, twit_with_media):
    user_1 = await UserFactory.create()
    user_2 = await UserFactory.create()
    user_3 = await UserFactory.create()
    await TwitFactory.create(user=user_1)
    twit_user_2 = await TwitFactory.create(user=user_2)
    twit_user_3 = await crud.twit.create_with_user(
        db, obj_in=twit_with_media, user_id=user_3.id
    )
    await FollowFactory.create(follower=user_1, following=user_2)
    await FollowFactory.create(follower=user_1, following=user_3)
    await LikeFactory.create(user=user_1, twit=twit_user_2)
    await LikeFactory.create(user=user_2, twit=twit_user_2)
    url = f'{settings.API_PREFIX_V1}/twits/'
    response = await client.get(url, headers={'api-key': user_1.key})
    assert response.status_code == 200
    json_response = {
        'result': True,
        'tweets': [
            {
                'id': twit_user_2.tweet_id,
                'content': twit_user_2.tweet_data,
                'attachments': [],
                'author': {'name': twit_user_2.user.name, 'id': twit_user_2.user.id},
                'likes': [
                    {'name': user_1.name, 'id': user_1.id},
                    {'name': user_2.name, 'id': user_2.id},
                ],
            },
            {
                'id': 4,
                'content': twit_user_3.tweet_data,
                'attachments': [f'{settings.MEDIA_URL}{m}' for m in twit_user_3.media],
                'author': {'name': user_3.name, 'id': user_3.id},
                'likes': [],
            },
        ],
    }
    assert response.json() == json_response
