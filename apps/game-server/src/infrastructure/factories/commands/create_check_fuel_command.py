from typing import Any

from src.application.commands.fuel_command import CheckFuelCommand
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.infrastructure.adapters.fuel_consumer_adapter import FuelConsumerAdapter


class CheckFuelObjectCommandFactory(IObjectCommandFactory):
    """
    Фабрика для команды проверки наличия достаточного количества топлива.
    Не использует аргументы из AgentMessage, так как логика зависит только
    от состояния объекта (fuel_level и fuel_consumption).
    """

    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        adapter = FuelConsumerAdapter(game_object)
        return CheckFuelCommand(adapter)
