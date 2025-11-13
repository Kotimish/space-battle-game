from typing import Mapping

from src.exceptions.security import SecurityException
from src.interfaces.operation_router import IOperationRouter
from src.interfaces.factories.object_command_factory import IObjectCommandFactory


class OperationToCommandRouter(IOperationRouter):
    """
    Роутер для сопоставления идентификаторов операций с классами фабрик команд.
    Обеспечивает безопасную маршрутизацию, разрешая только явно перечисленные операции.
    """
    def __init__(self, operation_map: Mapping[str, type[IObjectCommandFactory]]):
        """
        :param operation_map: Белый список разрешённых операций, где ключ — идентификатор операции,
                              а значение — класс фабрики, реализующей ICommandFactory и создающей
                              соответствующую команду.
        """
        self._operation_map = operation_map

    def get_factory(self, operation_id: str) -> type[IObjectCommandFactory]:
        """
        Возвращает класс фабрики для указанной операции.
        :param operation_id: Название операции
        :raises SecurityException: Если операция не входит в белый список.
        :return: Класс фабрики создания команды
        """
        if operation_id not in self._operation_map:
            raise SecurityException(f"Operation '{operation_id}' is not allowed")
        return self._operation_map[operation_id]