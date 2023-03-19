from fastapi import APIRouter

from src.api.api_v1.endpoints import media, twits, users
from src.core.api_responses import response_403, response_422

api_router = APIRouter(responses={**response_422, **response_403})
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(twits.router, prefix='/tweets', tags=['twits'])
api_router.include_router(media.router, prefix='/medias', tags=['media'])
