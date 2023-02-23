import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.db.base import Base
from src.models.user import User

engine = create_async_engine('postgresql+asyncpg://user:pass@localhost/dbtest')
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
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db(db_setup: AsyncGenerator) -> AsyncGenerator:
    """
    Create session before every test and rollback changes of this session at the end.
    """
    async with session() as sess:
        yield sess
        await sess.rollback()


@pytest_asyncio.fixture
async def create_user(db) -> None:
    user = User(name='Fix', key='test')
    db.add(user)
