from typing import Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.UserOut])
async def get_users(session: AsyncSession = Depends(deps.get_session)) -> Dict:
    users = await crud.user.get_multi(session)
    return users
