from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud.base import CRUDBase
from src.models import Twit


class CRUDTwit(CRUDBase[Twit, schemas.TwitBase]):
    async def create_with_user(
        self, db: AsyncSession, *, obj_in: schemas.TwitBase, user_id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        return db_obj


twit = CRUDTwit(Twit)
