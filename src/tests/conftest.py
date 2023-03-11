import asyncio
import os
from io import BytesIO
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.api.deps import get_session
from src.core.config import settings
from src.db.base import Base
from src.main import app
from src.models import Twit, User

engine = create_async_engine(
    settings.TEST_SQLALCHEMY_DATABASE_URI, echo=False  # type: ignore
)
session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


USER_API_KEY = 'test11'


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_setup() -> AsyncGenerator:
    """
    Create database models and drop after test session
    :return:
    """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await init_fixture_database()
        yield
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db(db_setup: AsyncConnection) -> AsyncGenerator:
    """
    Create session before every test and rollback changes of this session at the end.
    """
    async with session() as sess:
        yield sess
        await sess.rollback()


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url='http://localhost') as c:
        yield c


async def override_get_db():
    async with session() as sess:
        yield sess


async def init_fixture_database() -> None:
    async with session() as sess:
        async with sess.begin():
            user = User(name='Fix', key=USER_API_KEY)
            twit = Twit(tweet_data='text', user_id=1)
            sess.add_all([user, twit])
            await sess.commit()


@pytest.fixture
def user_api_key() -> dict:
    return {'api-key': USER_API_KEY}


@pytest.fixture
def file_fixture(request):
    name = request.param
    file_name = '%s%s' % (settings.MEDIA_ROOT, name)
    open(file_name, 'w').close()
    yield name
    os.remove(file_name)


@pytest_asyncio.fixture
async def uploaded_file():
    filename = 'asdfjhasdfk.jpeg'
    yield UploadFile(filename, BytesIO(b'binary_data'))
    os.remove(os.path.join(settings.MEDIA_ROOT, filename))


@pytest_asyncio.fixture
async def twit_with_media():
    from src.tests.factories import MediaFactory, TwitFactory

    media = await MediaFactory.create()
    twit = TwitFactory.build()
    obj_in = twit.to_json()
    obj_in.pop('user_id')
    obj_in['tweet_media_ids'] = [media.id]
    return obj_in


app.dependency_overrides[get_session] = override_get_db
