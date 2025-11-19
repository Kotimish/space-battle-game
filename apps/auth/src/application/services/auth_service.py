from datetime import datetime, timedelta, timezone
from typing import Tuple

from src.application.interfaces.jwt_service import IJWTService
from src.domain.interfaces.factories.auth_game_session_factory import IAuthGameSessionFactory
from src.domain.interfaces.repositories.auth_game_session_repository import IAuthGameSessionRepository
from src.domain.models.game_session import AuthGameSession
from src.infrastructure.config.settings import settings


class AuthService:
    def __init__(
            self,
            game_repository: IAuthGameSessionRepository,
            session_factory: IAuthGameSessionFactory,
            jwt_service: IJWTService
    ):
        self._repository = game_repository
        self._factory = session_factory
        self._jwt = jwt_service

    def create_game(self, organizer_id: str, participants: list[str]) -> AuthGameSession:
        session = self._factory.create(organizer_id, participants)
        self._repository.create(session)
        return session

    def issue_token(self, game_id: str, user_id: str) -> Tuple[str, datetime]:
        session = self._repository.get_by_id(game_id)
        if not session:
            raise ValueError("Game not found")
        if user_id not in session.participants:
            raise PermissionError("User is not a participant")

        # Рассчитываем время истечения
        expires_delta = timedelta(minutes=settings.jwt.access_token_expire_minutes)
        expires_at = datetime.now(timezone.utc) + expires_delta

        payload = {
            "sub": user_id,
            "game_id": game_id,
            "exp": expires_at
        }
        token = self._jwt.encode(payload)
        return token, expires_at
