from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.core.exceptions import ValidationError
from src.crud.base import CRUDBase
from src.models.user import User


class CRUDUser(CRUDBase[User, schemas.UserIn]):
    async def get_by_key(self, db: AsyncSession, *, key: str):
        query = select(self.model).filter_by(key=key)  # type: ignore
        user = await db.execute(query)
        user = user.scalars().first()
        if not user:
            raise ValidationError(self.model.__tablename__)
        return user

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, **kwargs
    ):
        query = (
            select(self.model)
            .filter_by(**kwargs)  # type: ignore
            .offset(skip)
            .limit(limit)
        )
        objects = await db.execute(query)
        return objects.scalars().unique().all()


user = CRUDUser(User)
