import uuid

from src.application.interfaces.factories.game_session_factory import IGameSessionFactory
from src.domain.models.game_session import GameSession


class GameSessionFactory(IGameSessionFactory):
    """Фабрики игровой сессии"""

    def create(self) -> GameSession:
        # Генерируем уникальный ID
        session_id = f"game_{str(uuid.uuid4())}"
        # Создаём сессию с этим ID
        session = GameSession(session_id)
        return session

    def create_with_id(self, game_id: str) -> GameSession:
        # Создаём сессию с предоставленным ID
        session = GameSession(game_id)
        return session
