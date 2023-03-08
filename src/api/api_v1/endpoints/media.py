from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post('/', response_model=schemas.MediaOut, status_code=201)
async def create_media(
    *,
    db: AsyncSession = Depends(deps.get_session),
    file: UploadFile,
    current_user: models.User = Depends(deps.get_current_user),
):
    file = await crud.media.create_with_user(
        db=db,
        file=file,
        user_id=current_user.id,
    )
    return file
