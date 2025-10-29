from abc import ABC, abstractmethod

from src.interfaces.base_command import BaseCommand


class ICommandHandler(ABC):
    """Единый интерфейс для всех реализаций обработчиков команд"""

    @abstractmethod
    def enqueue_command(self, cmd: BaseCommand) -> None:
        """Поместить команду в очередь на выполнение"""
        raise NotImplementedError

    @abstractmethod
    def dequeue_command(self) -> BaseCommand:
        """Получение первой команды из очереди"""
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """
        Запустить обработчик.
        - Для блокирующего: выполнить все команды и завершиться.
        - Для неблокирующего: запустить фоновый поток/event loop.
        """
        raise NotImplementedError


    @abstractmethod
    def stop(self) -> None:
        """Корректная остановка обработчика."""
        raise NotImplementedError
