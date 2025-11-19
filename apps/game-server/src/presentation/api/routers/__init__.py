__all__ = (
    'health_router',
    'games_router',
    'game_objects_router',
)

from src.presentation.api.routers.health_router import router as health_router
from src.presentation.api.routers.games_router import router as games_router
from src.presentation.api.routers.game_objects_router import router as game_objects_router
