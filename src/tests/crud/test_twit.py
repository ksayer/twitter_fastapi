import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.models.twit import Twit

pytestmark = pytest.mark.asyncio


async def test_fixture(db: AsyncSession):
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 1


async def test_get_twits(db: AsyncSession):
    twit = Twit(content='another content', user_id=1)
    db.add(twit)
    twits = await crud.twit.get_multi(db)
    assert len(twits) == 2
