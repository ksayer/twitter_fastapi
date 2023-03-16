from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.api import deps

router = APIRouter()


@router.post('/', response_model=schemas.MediaOut, status_code=201)
async def create_media(
    file: UploadFile,
    db: AsyncSession = Depends(deps.get_session),
):
    file = await crud.media.create_and_save_file(
        db=db,
        file=file,
    )
    return file
