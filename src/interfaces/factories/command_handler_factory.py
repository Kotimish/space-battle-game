from abc import ABC, abstractmethod

from src.interfaces.base_command import BaseCommand
from src.interfaces.command_handler import ICommandHandler

class ICommandHandlerFactory(ABC):
    """Интерфейс фабрики для создания экземпляров обработчиков команд."""
    @abstractmethod
    def create(self, scope_name: str, init_commands: list[BaseCommand]| None = None) -> ICommandHandler:
        """
         Создаёт и возвращает новый экземпляр обработчика команд.
        :param scope_name: Имя области видимости (scope), определяющее контекст создаваемого обработчика.
        :param init_commands: Список стартовых команд для обработчика команд.
        :return: Экземпляр класса, реализующего интерфейс ICommandHandler.
        """
        raise NotImplementedError