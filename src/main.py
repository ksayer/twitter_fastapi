import uvicorn
from fastapi import FastAPI

from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def hello_world():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app)
