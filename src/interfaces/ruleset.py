from abc import ABC, abstractmethod
from typing import Callable, Any

from src.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.interfaces.uobject import UObject
from src.models.game_session import GameSession


class IRuleset(ABC):
    """Интерфейс шаблона правил для игровой сессии"""

    @abstractmethod
    def get_initial_objects(self) -> dict[str, UObject]:
        """Возвращает начальные объекты (например, для теста — object_0)"""
        raise NotImplementedError

    @abstractmethod
    def get_allowed_operations(self) -> dict[str, type[IObjectCommandFactory]]:
        """Возвращает маппинг операций → фабрик"""
        raise NotImplementedError

    @abstractmethod
    def get_dependencies(self, game_id: str, session: GameSession) -> dict[str, Callable[..., Any]]:
        """
        Возвращает "карту зависимостей" — словарь {имя_зависимости: фабрика/лямбда}.
        Эти зависимости будут зарегистрированы в инфраструктурном слое.
        """
        raise NotImplementedError
