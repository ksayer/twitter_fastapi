import aiofiles
from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.exceptions import ValidationError
from src.crud.base import CreateSchemaType, CRUDBase
from src.models import Media
from src.utils import get_available_name


class CRUDMedia(CRUDBase[Media, CreateSchemaType]):
    async def create_and_save_file(
        self,
        db: AsyncSession,
        *,
        file: UploadFile,  # type: ignore
    ):
        """Create database row with given file name and create file in the disk"""
        filename = get_available_name(file.filename)
        path = settings.MEDIA_ROOT + filename
        content = file.file.read()
        async with aiofiles.open(path, 'wb') as new_file:
            await new_file.write(content)
        db_obj = self.model(file=filename)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_media(self, db: AsyncSession, ids: list[int]):
        """"""
        query = select(self.model).where(Media.id.in_(ids))
        result = await db.execute(query)
        media_list = result.scalars().all()
        if len(media_list) != len(ids):
            raise ValidationError(self.model.__tablename__)
        return media_list


media = CRUDMedia(Media)  # type: ignore
