from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post(
    '/',
    status_code=201,
    response_model=schemas.MediaOut,
    description='Upload media on server',
)
async def create_media(
    file: UploadFile,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
):
    file = await crud.media.create_and_save_file(
        db=db,
        file=file,
    )
    return file
