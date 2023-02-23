import uvicorn
from fastapi import FastAPI

from src.api.api_v1.api import api_router
from src.core.config import settings
from src.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(api_router, prefix=settings.API_PREFIX_V1)

if __name__ == "__main__":
    uvicorn.run(app)
