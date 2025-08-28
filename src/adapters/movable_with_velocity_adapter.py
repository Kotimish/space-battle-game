from src.adapters.movable_adapter import MovableObjectAdapter
from src.interfaces.mutable_velocity_object import IMutableVelocityObject
from src.interfaces.uobject import UObject
from src.models.vector import Vector


class MovableWithVelocityAdapter(MovableObjectAdapter, IMutableVelocityObject):
    """
    Адаптер для движущихся объектов
    с возможностью изменения вектора мгновенной скорости
    """
    def __init__(self, obj: UObject):
        super().__init__(obj)
        self.obj = obj

    def set_velocity(self, velocity: Vector) -> None:
        self.obj.set_property('velocity', velocity)
