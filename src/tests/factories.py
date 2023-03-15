from typing import Any

import factory
from factory import fuzzy

from src.models import Like, Media, Twit, User
from src.models.user import Follow
from src.tests.conftest import session


class AsyncAlchemyModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to use an async session.
        You must pass AsyncSession object in create method
        """
        async with session() as db:
            obj = model_class(*args, **kwargs)
            db.add(obj)
            await db.commit()
            return obj


class UserFactory(AsyncAlchemyModelFactory):
    class Meta:
        model = User

    name: Any = factory.Faker('first_name')
    key = fuzzy.FuzzyText(length=15)


class TwitFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Twit

    tweet_data = fuzzy.FuzzyText(length=15)
    user: Any = factory.SubFactory(UserFactory)

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to use an async session.
        You must pass AsyncSession object in create method
        """
        async with session() as db:
            user = kwargs.pop('user')
            user = user if isinstance(user, User) else await user
            obj = model_class(user=user, *args, **kwargs)
            db.add(obj)
            await db.commit()
            return obj


class MediaFactory(AsyncAlchemyModelFactory):
    class Meta:
        model = Media

    file: Any = factory.Faker('file_name')


class LikeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Like

    user: factory.SubFactory = factory.SubFactory(UserFactory)
    twit: factory.SubFactory = factory.SubFactory(TwitFactory)

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to use an async session.
        You must pass AsyncSession object in create method
        """
        async with session() as db:
            user = kwargs.pop('user')
            user = user if isinstance(user, User) else await user
            twit = kwargs.pop('twit')
            twit = twit if isinstance(twit, Twit) else await twit
            obj = model_class(user=user, twit=twit, *args, **kwargs)
            db.add(obj)
            await db.commit()
            return obj


class FollowFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Follow

    follower: factory.SubFactory = factory.SubFactory(UserFactory)
    following: factory.SubFactory = factory.SubFactory(UserFactory)

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to use an async session.
        You must pass AsyncSession object in create method
        """
        async with session() as db:
            follower = kwargs.pop('follower')
            follower = follower if isinstance(follower, User) else await follower
            following = kwargs.pop('following')
            following = following if isinstance(following, User) else await following
            obj = model_class(follower=follower, following=following, *args, **kwargs)
            db.add(obj)
            await db.commit()
            return obj
