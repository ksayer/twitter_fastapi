import aiofiles

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUDBase, CreateSchemaType
from src.models import Media
from src.core.config import settings
from src.utils import get_available_name


class CRUDMedia(CRUDBase[Media, CreateSchemaType]):
    async def create_with_user(
            self,
            db: AsyncSession,
            *,
            file: UploadFile,
            user_id: int,
    ):
        filename = get_available_name(file.filename)
        path = settings.MEDIA_ROOT + filename
        async with aiofiles.open(path, 'wb') as new_file:
            content = file.file.read()
            await new_file.write(content)
        db_obj = self.model(file=filename, user_id=user_id)
        db.add(db_obj)
        await db.commit()
        return db_obj


media = CRUDMedia(Media)
