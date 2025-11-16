from fastapi import APIRouter

from src.presentation.api.routers import health_router
from src.presentation.api.routers import games_router
from src.presentation.api.routers import game_objects_router

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

router.include_router(health_router)
router.include_router(games_router)
router.include_router(game_objects_router)
