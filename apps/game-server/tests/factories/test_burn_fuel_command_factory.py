from src.application.commands.fuel_command import BurnFuelCommand
from src.domain.models.uobject import DictUObject
from src.infrastructure.factories.commands import BurnFuelObjectCommandFactory


def test_burn_fuel_command_factory_creates_burn_fuel_command():
    """Тест создания фабрикой BurnFuelCommand с адаптером на основе UObject"""
    uobject = DictUObject({
        "fuel_level": 100,
        "fuel_consumption": 10
    })
    factory = BurnFuelObjectCommandFactory()
    command = factory.create(uobject, {})
    assert isinstance(command, BurnFuelCommand)
