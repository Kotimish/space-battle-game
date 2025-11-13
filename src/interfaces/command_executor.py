from abc import ABC, abstractmethod

from src.schemas.agent_message import AgentMessage


class ICommandExecutor(ABC):
    @abstractmethod
    def start(self, game_id: str, ruleset: str = "default") -> None:
        """Запускает обработчик команд для сессии"""
        raise NotImplementedError

    @abstractmethod
    def stop(self, game_id: str) -> None:
        """Останавливает обработчик"""
        raise NotImplementedError

    def stop_all(self) -> None:
        """Остановка всех игровых сессий"""
        raise NotImplementedError

    @abstractmethod
    def enqueue_interpret_command(self, game_id: str, message: AgentMessage) -> None:
        """Ставит InterpretCommand в очередь сессии"""
        raise NotImplementedError
