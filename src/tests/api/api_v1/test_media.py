import os

import pytest
from fastapi import UploadFile
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.crud import media

pytestmark = pytest.mark.asyncio


async def test_create_media(
    client: AsyncClient, db: AsyncSession, user_api_key: dict, uploaded_file: UploadFile
):
    file_data = {"file": (uploaded_file.filename, "file content")}
    response = await client.post(
        f"{settings.API_PREFIX_V1}/media/",
        headers=user_api_key,
        files=file_data,
    )
    file_in_db = await media.get_multi(db, file=uploaded_file.filename)
    assert response.status_code == 201
    assert os.path.exists(os.path.join(settings.MEDIA_ROOT, uploaded_file.filename))
    assert file_in_db[0].file == uploaded_file.filename
