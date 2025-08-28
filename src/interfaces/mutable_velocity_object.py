from abc import abstractmethod

from src.interfaces.movable_object import IMovableObject
from src.models.vector import Vector


class IMutableVelocityObject(IMovableObject):
    """Интерфейс для движущихся объектов с возможностью изменения скорости"""
    @abstractmethod
    def set_velocity(self, velocity: Vector) -> None:
        raise NotImplementedError
