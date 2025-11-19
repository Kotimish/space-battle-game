from typing import Any

from src.application.commands.rotate import RotateCommand
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.infrastructure.adapters.rotatable_adapter import RotatableObjectAdapter


class RotateCommandFactory(IObjectCommandFactory):
    """
    Фабрика для команды поворота объекта.
    Принимает UObject, оборачивает его в RotatableObjectAdapter.
    Предполагает, что UObject содержит все необходимые свойства:
    - angle, angular_velocity — для поворота.
    """

    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        # Создание адаптера
        rotatable = RotatableObjectAdapter(game_object)
        # Возврат команды
        return RotateCommand(rotatable)
