from src.exceptions.rotate import UnchangeableAngleError
from src.interfaces.base_command import BaseCommand
from src.interfaces.rotatable_object import IRotatableObject


class Rotate(BaseCommand):
    def __init__(self, rotatable: IRotatableObject):
        self._rotatable = rotatable

    def execute(self) -> None:
        angle = self._rotatable.get_angle()
        angular_velocity = self._rotatable.get_angular_velocity()
        new_angle = angle + angular_velocity
        if new_angle == angle:
            raise UnchangeableAngleError('The object has not changed angle.')
        self._rotatable.set_angle(angle + angular_velocity)
