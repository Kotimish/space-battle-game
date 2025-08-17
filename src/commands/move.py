from src.exceptions.move import UnchangeablePositionError
from src.interfaces.base_command import BaseCommand
from src.interfaces.movable_object import IMovableObject


class MoveCommand(BaseCommand):
    def __init__(self, movable: IMovableObject):
        self._movable = movable

    def execute(self) -> None:
        velocity = self._movable.get_velocity()
        position = self._movable.get_position()
        new_position = velocity + position
        if position == new_position:
            raise UnchangeablePositionError('The object has not changed position.')
        self._movable.set_position(velocity + position)
