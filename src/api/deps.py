from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud
from src.core.exceptions import ValidationError
from src.db.session import session


async def get_session():
    async with session() as sess:
        yield sess


async def get_current_user(
    db: AsyncSession = Depends(get_session),
    api_key: str = Header(description="Authorization by user's api-key"),
):
    user = await crud.user.get_or_none(db, key=api_key)
    if not user:
        raise ValidationError(
            message='required authorization', code=403, error_type='Forbidden'
        )
    return user
