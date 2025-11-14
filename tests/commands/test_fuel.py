import pytest

import src.application.commands.fuel_command as commands
import src.domain.exceptions.fuel_command as exceptions
from src.domain.exceptions.command import CommandException
from tests.factories import make_fuel_consumer_object


@pytest.mark.parametrize(
    'fuel_level, fuel_consumption',
    [
        (100, 10),
        (10, 10),
    ]
)
def test_check_fuel_with_valid_params(fuel_level: int, fuel_consumption: int):
    """
    Тест необходимого уровня топлива у объекта при достаточном уровне топлива
    """
    fuel_level = 0
    fuel_consumption = 0

    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    check_fuel = commands.CheckFuelCommand(fuel_consumer_object)
    check_fuel.execute()


@pytest.mark.parametrize(
    'fuel_level, fuel_consumption',
    [
        (10, 11),
    ]
)
def test_check_fuel_with_invalid_params(fuel_level: int, fuel_consumption: int):
    """
    Тест необходимого уровня топлива у объекта при недостаточном уровне топлива
    """
    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    check_fuel = commands.CheckFuelCommand(fuel_consumer_object)

    with pytest.raises(CommandException) as e:
        check_fuel.execute()


@pytest.mark.parametrize(
    'fuel_level, fuel_consumption, expected_fuel_level',
    [
        (100, 10, 90),
    ]
)
def test_burn_fuel_with_valid_params(fuel_level: int, fuel_consumption: int, expected_fuel_level: int):
    """Тест потребления топлива объектом"""
    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    burn_fuel = commands.BurnFuelCommand(fuel_consumer_object)
    burn_fuel.execute()

    assert fuel_consumer_object.get_fuel_level() == expected_fuel_level


def test_fuel_consumer_with_invalid_fuel_consumption():
    """Проверка объекта с неопределяемым уровнем потребления топлива"""
    fuel_level = 100
    fuel_consumption = None
    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    with pytest.raises(exceptions.UndefinedFuelConsumptionError) as e:
        fuel_consumer_object.get_fuel_consumption()


def test_fuel_consumer_with_invalid_fuel_level():
    """Проверка объекта с неопределяемым уровнем топлива"""
    fuel_level = None
    fuel_consumption = 100
    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    with pytest.raises(exceptions.UndefinedFuelLevelError) as e:
        fuel_consumer_object.get_fuel_level()
