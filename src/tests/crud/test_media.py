import os

import pytest
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.crud import media

pytestmark = pytest.mark.asyncio


async def test_create_media(db: AsyncSession, uploaded_file: UploadFile):
    await media.create_and_save_file(db, file=uploaded_file)
    file_in_db = await media.get_multi(db, file=uploaded_file.filename)
    assert file_in_db
    assert os.path.exists(os.path.join(settings.MEDIA_ROOT, uploaded_file.filename))
    assert file_in_db[0].file == uploaded_file.filename
