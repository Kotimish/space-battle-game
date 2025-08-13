from abc import ABC, abstractmethod
from src.models.vector import Vector


class IMovableObject(ABC):
    @abstractmethod
    def get_position(self) -> Vector:
        raise NotImplementedError

    @abstractmethod
    def get_velocity(self) -> Vector:
        raise NotImplementedError

    @abstractmethod
    def set_position(self, position: Vector) -> None:
        raise NotImplementedError
