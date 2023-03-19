from sqlalchemy import select

from src.db.base import User
from src.db.session import session as async_session


async def init_db() -> None:
    user = User(name='Nikolai', key='qwerty')
    user2 = User(name='Kate', key='ytrewq')
    user3 = User(name='Elon', key='test')
    async with async_session() as sesion:
        async with sesion.begin():
            users = await sesion.execute(select(User))
            if not users.scalars().unique().all():
                sesion.add_all([user, user2, user3])
                await sesion.commit()
