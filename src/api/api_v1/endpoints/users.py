from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get(
    "/me", status_code=200, response_model=dict[str, bool | schemas.UserOutFollowers]
)
async def get_my_info(
    *,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    user = await crud.user.get(db, key=current_user.key)
    return {'result': True, 'user': user}


@router.get(
    '/{id}', status_code=200, response_model=dict[str, bool | schemas.UserOutFollowers]
)
async def get_users_info(
    id: int,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
):
    user = await crud.user.get(db, id=id)
    return {'result': True, 'user': user}


@router.post('/{id}/follow/')
async def follow_user(
    id: int,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.follow.follow_user(
        db, following_user_id=id, follower_user_id=current_user.id
    )
    return {'result': True}


@router.delete('/{id}/follow/')
async def delete_follow_user(
    id: int,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.follow.delete_follow(
        db, following_user_id=id, follower_user_id=current_user.id
    )
    return {'result': True}
