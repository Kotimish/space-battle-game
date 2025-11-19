from abc import ABC, abstractmethod


class IDamageableObject(ABC):
    """Интерфейс для объектов, у которых есть параметр прочности"""

    @abstractmethod
    def get_health_points(self) -> int:
        """Получить уровень здоровья объекта"""
        raise NotImplementedError

    @abstractmethod
    def set_health_points(self, health_points: int) -> None:
        """Задать уровень здоровья объекта"""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Проверить существование объекта"""
        raise NotImplementedError
