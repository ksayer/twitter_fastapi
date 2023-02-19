from typing import Dict

import uvicorn
from fastapi import FastAPI

from src.core.config import settings
from src.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def hello_world() -> Dict:
    return {"hello": "world"}


@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app)
