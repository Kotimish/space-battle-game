# src/interfaces/operation_router.py
from abc import ABC, abstractmethod
from src.interfaces.factories.object_command_factory import IObjectCommandFactory


class IOperationRouter(ABC):
    """Интерфейс маршрутизатора операций к фабрикам команд."""
    @abstractmethod
    def get_factory(self, operation_id: str) -> type[IObjectCommandFactory]:
        """
        Возвращает класс фабрики команды по строковому идентификатору операции.
        :param operation_id: Идентификатор операции.
        :return: Класс - реализация ICommandFactory, который может создать
                 соответствующую команду на основе игрового объекта и аргументов.
        """
        raise NotImplementedError