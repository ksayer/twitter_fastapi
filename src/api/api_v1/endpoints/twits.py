from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post('/', response_model=schemas.TwitOut, status_code=201)
async def create_twit(
    *,
    db: AsyncSession = Depends(deps.get_session),
    twit_in: schemas.TwitBase,
    current_user: models.User = Depends(deps.get_current_user),
):
    twit = await crud.twit.create_with_user(
        db=db, obj_in=twit_in, user_id=current_user.id
    )
    return twit
