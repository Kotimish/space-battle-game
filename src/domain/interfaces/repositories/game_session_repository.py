from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models.game_session import GameSession

class IGameSessionRepository(ABC):
    """Интерфейс репозитория для игровой сессии GameSession."""
    @abstractmethod
    def add(self, session: GameSession) -> None:
        """
        Сохраняет новую сессию.
        :raises GameSessionAlreadyExistsException: Если сессия с указанным id уже существует.
        :raises GameSessionRepositoryAccessException: При ошибках доступа к хранилищу.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, session_id: str) -> Optional[GameSession]:
        """
        Находит сессию по ID.
        :raises GameSessionRepositoryAccessException: При ошибках доступа к хранилищу.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[GameSession]:
        """
        Получает список всех сессий.
        :raises GameSessionRepositoryAccessException: При ошибках доступа к хранилищу.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, session_id: str) -> bool:
        """
        Удаляет сессию по ID.
        :raises GameSessionRepositoryAccessException: При ошибках доступа к хранилищу.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_all(self) -> None:
        """
        Удаляет все сессии.
        :raises GameSessionRepositoryAccessException: При ошибках доступа к хранилищу.
        """
        raise NotImplementedError