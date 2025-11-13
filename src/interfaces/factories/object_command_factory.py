from abc import ABC, abstractmethod
from typing import Any

from src.interfaces.base_command import BaseCommand
from src.interfaces.uobject import UObject


class IObjectCommandFactory(ABC):
    """Интерфейс фабрики команд над объектами"""
    @abstractmethod
    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        """
        Создаёт команду, связанную с указанным игровым объектом.

        Метод может модифицировать состояние игрового объекта на основе переданных аргументов
        и затем вернуть сконфигурированную и готовую к выполнению команду.
        :param game_object: Игровой объект, над которым будет выполнена команда.
        :param arguments: Словарь аргументов, используемых для настройки команды или свойств объекта.
        :return: Готовый к выполнению экземпляр Команда
        """
        raise NotImplementedError
