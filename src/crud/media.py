import aiofiles
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.crud.base import CreateSchemaType, CRUDBase
from src.models import Media
from src.utils import get_available_name


class CRUDMedia(CRUDBase[Media, CreateSchemaType]):
    async def create(
        self,
        db: AsyncSession,
        *,
        file: UploadFile,
    ):
        filename = get_available_name(file.filename)
        path = settings.MEDIA_ROOT + filename
        content = file.file.read()
        async with aiofiles.open(path, 'wb') as new_file:
            await new_file.write(content)
        db_obj = self.model(file=filename)
        db.add(db_obj)
        await db.commit()
        return db_obj


media = CRUDMedia(Media)  # type: ignore
