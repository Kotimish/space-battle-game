from typing import Any

from src.application.commands.macro.rotate_with_velocity import RotateWithVelocityCommand
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.domain.models.angle import Angle
from src.infrastructure.adapters.movable_with_velocity_adapter import MovableWithVelocityAdapter
from src.infrastructure.adapters.rotatable_adapter import RotatableObjectAdapter


class RotateWithVelocityCommandFactory(IObjectCommandFactory):
    """
    Фабрика для макрокоманды поворота объекта с одновременным изменением
    вектора мгновенной скорости в соответствии с новым направлением.
    Предполагает, что UObject содержит все необходимые свойства:
    - angle, angular_velocity — для поворота;
    - position, velocity — для изменения скорости.
    """

    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        # Опционально: обновление angular_velocity из аргументов
        if "angular_velocity" in arguments:
            angular_velocity_data = arguments["angular_velocity"]
            angular_velocity = Angle.deserialize(angular_velocity_data)
            game_object.set_property("angular_velocity", angular_velocity)
        # Создаём два адаптера из одного UObject
        movable = MovableWithVelocityAdapter(game_object)
        rotatable = RotatableObjectAdapter(game_object)
        return RotateWithVelocityCommand(movable=movable, rotatable=rotatable)
