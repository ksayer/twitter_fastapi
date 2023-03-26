from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from src import crud, schemas
from src.core.exceptions import ValidationError
from src.crud.base import CRUDBase
from src.models import Like, MediaTwit, Twit, User
from src.models.user import Follow


class CRUDTwit(CRUDBase[Twit, schemas.TwitIn]):
    async def create_with_user(
        self, db: AsyncSession, *, obj_in: schemas.TwitIn, user_id: int
    ):
        """Create twit and add media to it if passed"""
        obj_in_data = jsonable_encoder(obj_in)
        media_ids = obj_in_data.pop('tweet_media_ids', [])
        media_list = await crud.media.get_media(db, media_ids) if media_ids else []
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db_obj.media.extend(media_list)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def delete_users_tweet(self, db: AsyncSession, twit_id: int, user_id: int):
        query = select(self.model).filter_by(  # type: ignore
            tweet_id=twit_id, user_id=user_id
        )
        user_twit = await db.execute(query)
        user_twit = user_twit.scalars().first()
        if not user_twit:
            raise ValidationError(self.model.__tablename__)
        await db.delete(user_twit)
        await db.commit()
        return True

    async def set_like(self, db: AsyncSession, twit_id: int, user_id: int):
        """Set like on twit, but If like exists - remove this like"""
        twit: Any = await self.get(db, tweet_id=twit_id)
        user = await crud.user.get(db, id=user_id)
        if user in twit.liked_users:
            twit.liked_users.remove(user)
        else:
            twit.liked_users.append(user)
        await db.commit()
        return twit

    async def delete_like(self, db: AsyncSession, twit_id: int, user_id: int):
        deleting_like = await crud.like.get(db, twit_id=twit_id, user_id=user_id)
        await db.delete(deleting_like)
        await db.commit()
        return True

    async def get_users_twits(
        self, db: AsyncSession, user_id: int, offset: int = 0, limit: int = 100
    ):
        followers_subquery = (
            select(Follow.following_id)
            .where(Follow.follower_id == user_id)
            .alias("followers")
        )
        query = (
            select(Twit)
            .options(  # type: ignore
                subqueryload(Twit.mediatwit).subqueryload(MediaTwit.media)
            )
            .join(User, onclause=Twit.user_id == User.id)
            .outerjoin(Like, Twit.tweet_id == Like.twit_id)
            .where(
                or_(
                    Twit.user_id == user_id,
                    Twit.user_id.in_(select(followers_subquery)),  # type: ignore
                )
            )
            .group_by(Twit.tweet_id)
            .offset(offset)
            .limit(limit)
            .order_by(desc(func.count(Like.user_id)), desc('tweet_id'))
        )
        twits = await db.execute(query)
        twits = twits.scalars().unique().all()
        return twits


twit = CRUDTwit(Twit)
