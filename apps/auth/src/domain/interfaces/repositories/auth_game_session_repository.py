from abc import ABC, abstractmethod
from typing import Optional

from src.domain.models.game_session import AuthGameSession


class IAuthGameSessionRepository(ABC):
    """
    Интерфейс репозитория для сессий авторизации.
    Хранит метаданные о том, какие пользователи участвуют в какой игре.
    """

    @abstractmethod
    def create(self, session: AuthGameSession) -> None:
        """
        Создаёт новую игровую сессию для авторизации.
        :param session: Сессия с game_id и participants.
        :raises ValueError: Если сессия с таким game_id уже существует.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, game_id: str) -> Optional[AuthGameSession]:
        """
        Находит сессию по game_id.
        :param game_id: Идентификатор игры.
        :return: Сессия или None.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all_game_ids(self) -> list[str]:
        """
        Возвращает список всех game_id.
        """
        raise NotImplementedError