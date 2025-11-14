import math

from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.mutable_velocity_object import IMutableVelocityObject
from src.domain.interfaces.rotatable_object import IRotatableObject
from src.domain.models.vector import Vector


class ChangeVelocityCommand(BaseCommand):
    """Команда изменения вектора мгновенной скорости при повороте"""
    def __init__(self, movable: IMutableVelocityObject, rotatable: IRotatableObject):
        self._movable = movable
        self._rotatable = rotatable

    def execute(self) -> None:
        velocity = self._movable.get_velocity()
        angular_velocity = self._rotatable.get_angular_velocity()
        angle_radians = angular_velocity.get_radians()
        cos_a = math.cos(angle_radians)
        sin_a = math.sin(angle_radians)
        new_velocity = Vector(
            round(velocity.x * cos_a - velocity.y * sin_a),
            round(velocity.y * cos_a + velocity.x * sin_a),
        )
        self._movable.set_velocity(new_velocity)