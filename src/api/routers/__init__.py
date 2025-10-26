__all__ = (
    'health_router',
    'agent_router',
)

from src.api.routers.health_router import router as health_router
from src.api.routers.agent_router import router as agent_router
