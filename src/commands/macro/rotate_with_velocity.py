from src.commands.change_velocity_command import ChangeVelocityCommand
from src.commands.macro.macro_command import MacroCommand
from src.commands.rotate import RotateCommand
from src.interfaces.mutable_velocity_object import IMutableVelocityObject
from src.interfaces.rotatable_object import IRotatableObject


class RotateWithVelocityCommand(MacroCommand):
    """Макро-Команда поворота объекта с изменением вектора мгновенной скорости при повороте"""
    def __init__(self, movable: IMutableVelocityObject, rotatable: IRotatableObject):
        self._movable = movable
        self._rotatable = rotatable
        self._commands = [
            RotateCommand(rotatable),
            ChangeVelocityCommand(movable, rotatable)
        ]

        super().__init__(self._commands)