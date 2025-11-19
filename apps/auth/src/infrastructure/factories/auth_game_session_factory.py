import uuid
from datetime import datetime, timezone

from src.domain.interfaces.factories.auth_game_session_factory import IAuthGameSessionFactory
from src.domain.models.game_session import AuthGameSession


class InMemoryAuthGameSessionFactory(IAuthGameSessionFactory):
    def create(self, organizer_id: str, participants: list[str]) -> AuthGameSession:
        game_id = f"battle_{uuid.uuid4()}"
        return AuthGameSession(
            game_id=game_id,
            organizer_id=organizer_id,
            participants=participants,
            created_at=datetime.now(timezone.utc)
        )
