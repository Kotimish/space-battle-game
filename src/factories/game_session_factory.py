import uuid

from src.dependencies.ioc import IoC
from src.interfaces.base_command import BaseCommand
from src.interfaces.factories.command_handler_factory import ICommandHandlerFactory
from src.interfaces.factories.game_session_factory import IGameSessionFactory
from src.models.game_session import GameSession


class GameSessionFactory(IGameSessionFactory):
    """Фабрики игровой сессии"""
    def create(self) -> GameSession:
        # Генерируем уникальный ID
        session_id = f"game_{str(uuid.uuid4())}"
        # Создаём сессию с этим ID
        session = GameSession(session_id)
        return session
