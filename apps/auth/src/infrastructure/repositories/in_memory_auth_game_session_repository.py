from threading import Lock
from typing import Optional, List
from src.domain.interfaces.repositories.auth_game_session_repository import IAuthGameSessionRepository
from src.domain.models.game_session import AuthGameSession


class InMemoryAuthGameSessionRepository(IAuthGameSessionRepository):
    """
    In-Memory реализация репозитория сессий авторизации.
    Используется только в рамках одного экземпляра сервиса.
    """

    def __init__(self):
        self._sessions: dict[str, AuthGameSession] = {}
        self._lock = Lock()

    def create(self, session: AuthGameSession) -> None:
        with self._lock:
            if session.game_id in self._sessions:
                raise ValueError(f"Session with game_id '{session.game_id}' already exists")
            self._sessions[session.game_id] = session

    def get_by_id(self, game_id: str) -> Optional[AuthGameSession]:
        with self._lock:
            return self._sessions.get(game_id)

    def get_all_game_ids(self) -> List[str]:
        with self._lock:
            return list(self._sessions.keys())