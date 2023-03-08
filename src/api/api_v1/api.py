from fastapi import APIRouter

from src.api.api_v1.endpoints import twits, users, media

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(twits.router, prefix='/twits', tags=['twits'])
api_router.include_router(media.router, prefix='/media', tags=['media'])
