from typing import Any

from src.infrastructure.adapters.move_fuel_consumer_adapter import MoveFuelConsumer
from src.application.commands.macro.move_with_fuel_command import MoveWithFuelCommand
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.domain.models.vector import Vector


class MoveWithFuelObjectCommandFactory(IObjectCommandFactory):
    """Фабрика для макро-команды движения по прямой с расходом топлива"""
    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        if "velocity" in arguments:
            velocity = Vector.deserialize(arguments.get('velocity'))
            game_object.set_property('velocity', velocity)
        adapter = MoveFuelConsumer(game_object)
        return MoveWithFuelCommand(adapter)
