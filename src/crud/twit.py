from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from sqlalchemy import exists, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud.base import CRUDBase
from src.models import Twit, Media


class CRUDTwit(CRUDBase[Twit, schemas.TwitBase]):
    async def create_with_user(
        self, db: AsyncSession, *, obj_in: schemas.TwitBase, user_id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        media_ids = obj_in_data.pop('tweet_media_ids')
        if media_ids:
            await self.validate_ids(db, media_ids)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def validate_ids(self, db, ids):
        query = select(func.count(Media.id)).where(Media.id.in_(ids))
        result = await db.execute(query)
        if result.scalars().first() != len(ids):
            raise HTTPException(status_code=404, detail="media not found")


twit = CRUDTwit(Twit)
