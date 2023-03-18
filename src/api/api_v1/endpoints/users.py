from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, models, schemas
from src.api import deps
from src.core.api_responses import simple_response_200

router = APIRouter()


@router.get(
    "/me",
    status_code=200,
    response_model=schemas.UserOutFollowersResponse,
    description='Get information about current user',
)
async def get_my_info(
    *,
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    user = await crud.user.get(db, key=current_user.key)
    return {'user': user}


@router.get(
    '/{id}',
    status_code=200,
    response_model=schemas.UserOutFollowersResponse,
    description='Get information about user by ID',
)
async def get_users_info(
    id: Annotated[int, Path(description="ID of the user we are looking for")],
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    user = await crud.user.get(db, id=id)
    return {'user': user}


@router.post(
    '/{id}/follow/',
    status_code=200,
    responses={**simple_response_200},
    description='Follow user by ID',
)
async def follow_user(
    id: Annotated[int, Path(description="ID of the user we are following")],
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.follow.follow_user(
        db, following_user_id=id, follower_user_id=current_user.id
    )
    return {'result': True}


@router.delete(
    '/{id}/follow/',
    status_code=200,
    responses={**simple_response_200},
    description='Stop following user',
)
async def delete_follow_user(
    id: Annotated[int, Path(description="ID of the user we are unfollowing from")],
    db: AsyncSession = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_user),
) -> dict:
    await crud.follow.delete_follow(
        db, following_user_id=id, follower_user_id=current_user.id
    )
    return {'result': True}
