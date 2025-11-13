from typing import Any

from src.adapters.movable_adapter import MovableObjectAdapter
from src.commands.move import MoveCommand
from src.interfaces.base_command import BaseCommand
from src.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.interfaces.uobject import UObject
from src.models.vector import Vector


class MoveObjectCommandFactory(IObjectCommandFactory):
    """Фабрика для команды движения"""
    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        if "velocity" in arguments:
            velocity = Vector.deserialize(arguments.get('velocity'))
            game_object.set_property('velocity', velocity)
        adapter = MovableObjectAdapter(game_object)
        return MoveCommand(adapter)
