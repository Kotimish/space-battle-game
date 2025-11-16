from threading import Lock
from typing import Dict, Optional

from src.infrastructure.exceptions import game_session_repository as exceptions
from src.domain.interfaces.repositories.game_session_repository import IGameSessionRepository
from src.domain.models.game_session import GameSession


class InMemoryGameSessionRepository(IGameSessionRepository):
    """
    In-Memory реализация репозитория GameSession.
    Хранит сессии в памяти.
    """

    def __init__(self):
        self._sessions: Dict[str, GameSession] = {}
        # Для потокобезопасности
        self._lock = Lock()

    def add(self, session: GameSession) -> None:
        with self._lock:
            if session.id in self._sessions:
                raise exceptions.GameSessionAlreadyExistsException(
                    f"Game session with ID {session.id} already exists in repository."
                )
            self._sessions[session.id] = session

    def get_by_id(self, session_id: str) -> Optional[GameSession]:
        with self._lock:
            return self._sessions.get(session_id, None)

    def get_all(self) -> list[GameSession]:
        with self._lock:
            # Возвращаем копию
            return list(self._sessions.values())

    def remove(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._sessions:
                self._sessions.pop(session_id)
                return True
            return False

    def remove_all(self) -> None:
        with self._lock:
            self._sessions.clear()
