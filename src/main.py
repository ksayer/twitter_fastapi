from typing import Dict, List

import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src import crud, schemas
from src.api import deps
from src.core.config import settings
from src.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/users", response_model=List[schemas.UserOut])
async def get_users(session: AsyncSession = Depends(deps.get_session)) -> Dict:
    users = await crud.user.get_all_users(session)
    return users


@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app)
