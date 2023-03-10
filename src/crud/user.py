from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud.base import CRUDBase
from src.models.user import User


class CRUDUser(CRUDBase[User, schemas.UserBase]):
    async def get_by_key(self, db: AsyncSession, *, key: str):
        query = select(self.model).filter_by(key=key)  # type: ignore
        user = await db.execute(query)
        user = user.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail='user not found')
        return user


user = CRUDUser(User)
