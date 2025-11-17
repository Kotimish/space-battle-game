from abc import ABC, abstractmethod

from src.domain.models.game_session import AuthGameSession


class IAuthGameSessionFactory(ABC):
    @abstractmethod
    def create(self, participants: list[str]) -> AuthGameSession:
        raise NotImplementedError
