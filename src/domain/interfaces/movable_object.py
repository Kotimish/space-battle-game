from abc import ABC, abstractmethod
from src.domain.models.vector import Vector


class IMovableObject(ABC):
    """Интерфейс для движущихся объектов"""
    @abstractmethod
    def get_position(self) -> Vector:
        """Получение позиции объекта"""
        raise NotImplementedError

    @abstractmethod
    def get_velocity(self) -> Vector:
        """Получения скорости объекта"""
        raise NotImplementedError

    @abstractmethod
    def set_position(self, position: Vector) -> None:
        """Изменения позиции объекта"""
        raise NotImplementedError
