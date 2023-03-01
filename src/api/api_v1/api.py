from fastapi import APIRouter

from src.api.api_v1.endpoints import twits, users

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(twits.router, prefix='/twits', tags=['twits'])
