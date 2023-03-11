from typing import Any

import factory
from factory import fuzzy

from src.models import Media, Twit, User
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
            user = await kwargs.pop('user')
            obj = model_class(user=user, *args, **kwargs)
            db.add(obj)
            await db.commit()
            return obj


class MediaFactory(AsyncAlchemyModelFactory):
    class Meta:
        model = Media

    file: Any = factory.Faker('file_name')