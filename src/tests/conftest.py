import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.api.deps import get_session
from src.core.config import settings
from src.db.base import Base
from src.main import app
from src.models.user import User

engine = create_async_engine(
    settings.TEST_SQLALCHEMY_DATABASE_URI, echo=False
)
session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Creates an instance of the default event loop for the test session.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_setup() -> AsyncGenerator:
    """
    Create database models and drop after test session
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await init_fixture_database()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db(db_setup: AsyncConnection) -> AsyncGenerator:
    """
    Create session before every test and rollback changes of this session at the end.
    """
    async with session() as sess:
        async with sess.begin():
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
            user = User(name='Fix', key='test11')
            sess.add(user)
            await sess.commit()


app.dependency_overrides[get_session] = override_get_db
