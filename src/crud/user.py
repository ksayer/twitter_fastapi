from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud.base import CRUDBase
from src.models.user import User


class CRUDUser(CRUDBase[User, schemas.UserBase]):
    async def get_by_key(self, db: AsyncSession, *, key: str):
        query = select(self.model).filter_by(key=key)  # type: ignore
        user = await db.execute(query)
        return user.scalars().first()


user = CRUDUser(User)
