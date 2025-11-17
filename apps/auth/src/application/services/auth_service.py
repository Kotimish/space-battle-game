from datetime import datetime, timedelta, timezone

from src.application.interfaces.jwt_service import IJWTService
from src.domain.interfaces.factories.auth_game_session_factory import IAuthGameSessionFactory
from src.domain.interfaces.repositories.auth_game_session_repository import IAuthGameSessionRepository
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

    def create_game(self, participants: list[str]):
        session = self._factory.create(participants)
        self._repository.create(session)
        return session.game_id

    def issue_token(self, game_id: str, user_id: str) -> str:
        session = self._repository.get_by_id(game_id)
        if not session:
            raise ValueError("Game not found")
        if user_id not in session.participants:
            raise PermissionError("User is not a participant")
        payload = {
            "sub": user_id,
            "game_id": game_id,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.jwt.access_token_expire_minutes)
        }
        return self._jwt.encode(payload)
