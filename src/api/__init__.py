from fastapi import APIRouter

from src.api.routers import health_router
from src.api.routers import agent_router

router = APIRouter()
router.include_router(health_router)
router.include_router(agent_router)
