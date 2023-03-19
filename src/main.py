import pkg_resources
import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.api.api_v1.api import api_router
from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.db.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME, docs_url='/api/docs', redoc_url=None)
register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_PREFIX_V1)
app.mount("/static", StaticFiles(directory="static"))

templates = Jinja2Templates(directory="static")


@app.get("/", include_in_schema=False)
def root():
    return HTMLResponse(pkg_resources.resource_string(__name__, 'static/index.html'))


@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(app)
