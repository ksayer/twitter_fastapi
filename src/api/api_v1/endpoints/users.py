from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas, models
from src.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.UserOut])
async def get_users(session: AsyncSession = Depends(deps.get_session)) -> Dict:
    users = await crud.user.get_multi(session)
    return users


@router.post('/{id}/follow/')
async def follow_user(
    *,
    db: AsyncSession = Depends(deps.get_session),
    id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    await crud.follow.follow_user(
        db, following_user_id=id, follower_user_id=current_user.id
    )
    return {'result': True}


@router.delete('/{id}/follow/')
async def delete_follow_user(
    *,
    db: AsyncSession = Depends(deps.get_session),
    id: int,
    current_user: models.User = Depends(deps.get_current_user)
):
    await crud.follow.delete_follow(
        db, following_user_id=id, follower_user_id=current_user.id
    )
    return {'result': True}
