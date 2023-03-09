from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy import exists, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud.base import CRUDBase
from src.models import Twit, Media


class CRUDTwit(CRUDBase[Twit, schemas.TwitIn]):
    async def create_with_user(
        self, db: AsyncSession, *, obj_in: schemas.TwitIn, user_id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        media_ids = obj_in_data.pop('tweet_media_ids')
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


twit = CRUDTwit(Twit)
