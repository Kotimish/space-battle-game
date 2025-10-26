from typing import Any

from src.adapters.move_fuel_consumer_adapter import MoveFuelConsumer
from src.commands.macro.move_with_fuel_command import MoveWithFuelCommand
from src.interfaces.base_command import BaseCommand
from src.interfaces.command_factory import ICommandFactory
from src.interfaces.uobject import UObject
from src.models.vector import Vector


class MoveWithFuelCommandFactory(ICommandFactory):
    """Фабрика для макро-команды движения по прямой с расходом топлива"""
    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        if "velocity" in arguments:
            velocity = Vector.from_dict(arguments.get('velocity'))
            game_object.set_property('velocity', velocity)
        adapter = MoveFuelConsumer(game_object)
        return MoveWithFuelCommand(adapter)
