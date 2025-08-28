import pytest

from src.commands.fuel_command import CheckFuelCommand, BurnFuelCommand
from src.commands.macro_command import MacroCommand
from src.commands.move import MoveCommand
from src.exceptions.command import CommandException
from src.models.vector import Vector
from tests.test_fuel import make_fuel_consumer_object
from tests.test_move import make_movable_object


def test_macro_command_with_valid_params():
    """Тест простейшей макро-команды с помощью команд движения и сжигания топлива"""
    start_position = Vector(0, 0)
    velocity = Vector(10, 0)
    expected_position = Vector(10, 0)

    fuel_level = 100
    fuel_consumption = 10
    expected_fuel_level = 90

    movable_object = make_movable_object(start_position, velocity)
    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    commands = [
        CheckFuelCommand(fuel_consumer_object),
        MoveCommand(movable_object),
        BurnFuelCommand(fuel_consumer_object)
    ]
    macro_command = MacroCommand(commands)
    macro_command.execute()

    assert movable_object.get_position() == expected_position
    assert fuel_consumer_object.get_fuel_level() == expected_fuel_level


@pytest.mark.parametrize(
    'start_position, velocity',
    [
        (Vector(0, 0), Vector(10, 0)),
        (Vector(10, 0), Vector(0, 0)),
    ]
)
def test_macro_command_with_invalid_params(start_position: Vector, velocity: Vector):
    """Тест работы макро-команды с вызовом ошибки"""
    fuel_level = 10
    fuel_consumption = 100

    movable_object = make_movable_object(start_position, velocity)
    fuel_consumer_object = make_fuel_consumer_object(fuel_level, fuel_consumption)
    commands = [
        CheckFuelCommand(fuel_consumer_object),
        MoveCommand(movable_object),
        BurnFuelCommand(fuel_consumer_object)
    ]
    macro_command = MacroCommand(commands)
    with pytest.raises(CommandException) as e:
        macro_command.execute()
