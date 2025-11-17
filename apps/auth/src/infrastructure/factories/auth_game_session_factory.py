import uuid

from src.domain.interfaces.factories.auth_game_session_factory import IAuthGameSessionFactory
from src.domain.models.game_session import AuthGameSession


class InMemoryAuthGameSessionFactory(IAuthGameSessionFactory):
    def create(self, participants: list[str]) -> AuthGameSession:
        game_id = f"battle_{uuid.uuid4()}"
        return AuthGameSession(game_id=game_id, participants=participants)
