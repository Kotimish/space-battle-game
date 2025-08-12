from abc import ABC, abstractmethod
from src.models.angle import Angle


class IRotatableObject(ABC):
    @abstractmethod
    def get_angle(self) -> Angle:
        raise NotImplementedError

    @abstractmethod
    def get_angular_velocity(self) -> Angle:
        raise NotImplementedError

    @abstractmethod
    def set_angle(self, angle: Angle) -> None:
        raise NotImplementedError
