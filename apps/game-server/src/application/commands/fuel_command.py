from src.domain.exceptions.command import CommandException
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.fuel_consumer_object import IFuelConsumerObject


class CheckFuelCommand(BaseCommand):
    """Команда проверки достаточного количества топлива"""
    def __init__(self, fuel_consumer: IFuelConsumerObject):
        self._fuel_consumer = fuel_consumer

    def execute(self) -> None:
        fuel_level = self._fuel_consumer.get_fuel_level()
        required_fuel_level = self._fuel_consumer.get_fuel_consumption()
        if fuel_level < required_fuel_level:
            raise CommandException(
                f'Not enough fuel: {required_fuel_level} fuel needed, but {fuel_level} fuel available'
            )


class BurnFuelCommand(BaseCommand):
    """Команда уменьшения количества топлива на скорость расхода топлива"""
    def __init__(self, fuel_consumer: IFuelConsumerObject):
        self._fuel_consumer = fuel_consumer

    def execute(self) -> None:
        fuel_level = self._fuel_consumer.get_fuel_level()
        required_fuel_level = self._fuel_consumer.get_fuel_consumption()
        new_fuel_level = fuel_level - required_fuel_level
        self._fuel_consumer.set_fuel_level(new_fuel_level)
