from src.application.commands.fuel_command import CheckFuelCommand
from src.domain.models.uobject import DictUObject
from src.infrastructure.factories.commands import CheckFuelObjectCommandFactory


def test_check_fuel_command_factory_creates_check_fuel_command():
    """Тест создания фабрикой CheckFuelCommand с адаптером на основе UObject"""
    uobject = DictUObject({
        "fuel_level": 100,
        "fuel_consumption": 10
    })
    factory = CheckFuelObjectCommandFactory()
    command = factory.create(uobject, {})
    assert isinstance(command, CheckFuelCommand)
