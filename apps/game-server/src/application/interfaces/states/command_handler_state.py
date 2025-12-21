from abc import ABC, abstractmethod
from queue import Queue

from src.domain.interfaces.base_command import BaseCommand
from src.infrastructure.handlers.exception_handler import ExceptionHandler


class ICommandHandlerState(ABC):
    """Интерфейс состояний обработчика очереди команд"""

    @abstractmethod
    def handle(
            self,
            queue: Queue[BaseCommand],
            exception_handler: ExceptionHandler
    ) -> 'ICommandHandlerState | None':
        raise NotImplementedError
