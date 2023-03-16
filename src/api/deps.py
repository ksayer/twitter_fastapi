from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.db.session import session


async def get_session():
    async with session() as sess:
        yield sess


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    api_key: str = Header(),
):
    user = await crud.user.get(db, key=api_key)
    return user
