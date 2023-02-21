from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class CRUDUser:
    def __init__(self, model: Type[User]):
        self.model = model

    async def get_all_users(self, db: AsyncSession):
        query = select(self.model)
        users = await db.execute(query)
        return users.scalars().all()


user = CRUDUser(User)
