from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps
from src.core.api_responses import simple_response_200

router = APIRouter()


@router.post(
    '/',
    status_code=201,
    response_model=schemas.TwitOut,
)
async def create_twit(
    twit_in: schemas.TwitIn,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    twit = await crud.twit.create_with_user(
        db=db, obj_in=twit_in, user_id=current_user.id
    )
    return twit


@router.delete(
    '/{id}/',
    status_code=200,
    responses={**simple_response_200},
    description='Delete the twit',
)
async def delete_users_twit(
    id: int = Path(description="ID of the deleting twit"),
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.twit.delete_users_tweet(db, twit_id=id, user_id=current_user.id)
    return {'result': True}


@router.post(
    '/{id}/likes/',
    status_code=200,
    responses={**simple_response_200},
    description='Like the twit',
)
async def set_like(
    id: int = Path(description="ID of the twit"),
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
):
    await crud.twit.set_like(db, twit_id=id, user_id=current_user.id)
    return {'result': True}


@router.delete(
    '/{id}/likes/',
    status_code=200,
    responses={**simple_response_200},
    description='Unlike the twit',
)
async def delete_like(
    id: int = Path(description="ID of the twit"),
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.twit.delete_like(db, twit_id=id, user_id=current_user.id)
    return {'result': True}


@router.get(
    '/',
    status_code=200,
    response_model=schemas.TwitOutFeedListResponse,
    description="Get all twits of current user' followings",
)
async def get_users_twits(
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    twits = await crud.twit.get_users_twits(db, user_id=current_user.id)
    return {"tweets": twits}
