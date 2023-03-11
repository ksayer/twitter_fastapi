from typing import Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.crud.base import CRUDBase
from src.models import Media, Twit


class CRUDTwit(CRUDBase[Twit, schemas.TwitIn]):
    async def create_with_user(
        self, db: AsyncSession, *, obj_in: schemas.TwitIn, user_id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        media_ids = obj_in_data.pop('tweet_media_ids', [])
        media_list = await self.get_media(db, media_ids) if media_ids else []
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db_obj.media.extend(media_list)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_media(self, db: AsyncSession, ids: list[int]):
        query = select(Media).where(Media.id.in_(ids))
        result = await db.execute(query)
        media_list = result.scalars().all()
        if len(media_list) != len(ids):
            raise HTTPException(status_code=404, detail="media not found")
        return media_list

    async def delete_users_tweet(self, db: AsyncSession, twit_id: int, user_id: int):
        query = select(self.model).filter_by(  # type: ignore
            tweet_id=twit_id, user_id=user_id
        )
        user_twit = await db.execute(query)
        user_twit = user_twit.scalars().first()
        if not user_twit:
            raise HTTPException(status_code=404, detail="twit not found")
        await db.delete(user_twit)
        await db.commit()
        return True

    async def set_like(self, db: AsyncSession, twit_id: int, user_id: int):
        twit: Any = await self.get(db, tweet_id=twit_id)
        user = await crud.user.get(db, id=user_id)
        if user in twit.likes:
            raise HTTPException(status_code=400, detail='Like already set')
        twit.likes.append(user)
        await db.commit()
        return twit


twit = CRUDTwit(Twit)
