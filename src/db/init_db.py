from sqlalchemy import select

from src.db.base import User
from src.db.session import session as async_session
from src.models import Twit
from src.models.user import Follow


async def init_db() -> None:
    user = User(name='Deelon', key='test')
    user_2 = User(name='Nikolai', key='test2')
    user_3 = User(name='Kate', key='test3')
    t_1 = Twit(user=user, tweet_data="Hello there! I'm Deelon")
    t_2 = Twit(user=user_2, tweet_data="Hello there! I'm Nikolai")
    t_3 = Twit(user=user_3, tweet_data="Hello there! I'm Kate")
    f_1 = Follow(follower=user, following=user_2)
    f_2 = Follow(follower=user, following=user_3)
    f_3 = Follow(follower=user_2, following=user_3)
    f_4 = Follow(follower=user_3, following=user)
    async with async_session() as sesion:
        async with sesion.begin():
            users = await sesion.execute(select(User))
            if not users.scalars().unique().all():
                sesion.add_all(
                    [user, user_2, user_3, t_1, t_2, t_3, f_1, f_2, f_3, f_4]
                )
                await sesion.commit()
