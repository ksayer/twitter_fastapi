import os

import pytest
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.crud import media

pytestmark = pytest.mark.asyncio


async def test_create_media(db: AsyncSession, uploaded_file: UploadFile):
    await media.create_with_user(db, file=uploaded_file, user_id=1)
    file_in_db = await media.get_multi(db, file=uploaded_file.filename)
    assert file_in_db
    assert os.path.exists(os.path.join(settings.MEDIA_ROOT, uploaded_file.filename))
    assert file_in_db[0].user_id == 1
    assert file_in_db[0].user_id == 1 and file_in_db[0].file == uploaded_file.filename