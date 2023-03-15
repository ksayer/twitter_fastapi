from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.post('/', response_model=schemas.TwitOut, status_code=201)
async def create_twit(
    *,
    db: AsyncSession = Depends(deps.get_session),
    twit_in: schemas.TwitIn,
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    twit = await crud.twit.create_with_user(
        db=db, obj_in=twit_in, user_id=current_user.id
    )
    return twit


@router.delete('/{id}/', status_code=200)
async def delete_users_twit(
    *,
    db: AsyncSession = Depends(deps.get_session),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.twit.delete_users_tweet(db, twit_id=id, user_id=current_user.id)
    return {'result': True}


@router.post('/{id}/likes/', status_code=200)
async def set_like(
    *,
    db: AsyncSession = Depends(deps.get_session),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    await crud.twit.set_like(db, twit_id=id, user_id=current_user.id)
    return {'result': True}


@router.delete('/{id}/likes/', status_code=200)
async def delete_like(
    *,
    db: AsyncSession = Depends(deps.get_session),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.twit.delete_like(db, twit_id=id, user_id=current_user.id)
    return {'result': True}


@router.get(
    '/', status_code=200, response_model=dict[str, bool | list[schemas.TwitOutFeed]]
)
async def get_users_twits(
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    twits = await crud.twit.get_users_twits(db, user_id=current_user.id)
    return {"result": True, "tweets": twits}
