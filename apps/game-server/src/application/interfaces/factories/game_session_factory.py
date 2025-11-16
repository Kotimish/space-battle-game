from abc import ABC, abstractmethod
from src.domain.models.game_session import GameSession


class IGameSessionFactory(ABC):
    """Интерфейс фабрики для создания игровых сессий."""
    @abstractmethod
    def create(self) -> GameSession:
        """
        Создаёт и возвращает новый экземпляр игровой сессии.
        :return: Экземпляр класса GameSession.
        """
        raise NotImplementedError
