from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.services.auth_service import AuthService
from src.infrastructure.config.settings import settings
from src.infrastructure.factories.auth_game_session_factory import InMemoryAuthGameSessionFactory
from src.infrastructure.repositories.in_memory_auth_game_session_repository import InMemoryAuthGameSessionRepository
from src.infrastructure.security.jwt_service import PyJWTService


def setup_auth_service() -> AuthService:
    """Собирает AuthService с конкретными реализациями."""
    repo = InMemoryAuthGameSessionRepository()
    factory = InMemoryAuthGameSessionFactory()
    jwt_service = PyJWTService(
        secret=settings.jwt.secret,
        algorithm=settings.jwt.algorithm,
        expire_minutes=settings.jwt.access_token_expire_minutes
    )
    return AuthService(
        game_repository=repo,
        session_factory=factory,
        jwt_service=jwt_service
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup
    app.state.auth_service = setup_auth_service()
    yield
    # Teardown
    app.state.auth_service = None
