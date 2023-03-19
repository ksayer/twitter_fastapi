import os

import pkg_resources
import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from src.api.api_v1.api import api_router
from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME, docs_url='/api/docs', redoc_url=None)
app.include_router(api_router, prefix=settings.API_PREFIX_V1)
register_exception_handlers(app)


app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    ),
)


@app.get("/", include_in_schema=False)
def root():
    return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))


@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app)
