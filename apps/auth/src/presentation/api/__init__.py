from fastapi import APIRouter

from src.presentation.api.routers.auth_router import router as auth_router
from src.presentation.api.routers.games_router import router as games_router
from src.presentation.api.routers.health_router import router as health_router

api_router = APIRouter(prefix="/api")
api_router.include_router(games_router)
api_router.include_router(auth_router)
api_router.include_router(health_router)
