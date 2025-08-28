import pytest

from src.adapters.move_fuel_consumer_adapter import MoveFuelConsumer
from src.commands.move_with_fuel_command import MoveWithFuelCommand
from src.exceptions.command import CommandException
from src.interfaces.move_fuel_consumer import IMoveFuelConsumer
from src.models.vector import Vector
from tests.mock_object import MockUObject


def make_movable_fuel_consumer(
        position: Vector,
        velocity: Vector,
        fuel_level: int,
        fuel_consumption: int
) -> IMoveFuelConsumer:
    data = {
        "position": position,
        "velocity": velocity,
        "fuel_level": fuel_level,
        "fuel_consumption": fuel_consumption
    }
    mock_object = MockUObject(data)
    movable_object = MoveFuelConsumer(mock_object)
    return movable_object



def test_macro_command_with_valid_params():
    """Тест макро-команды с помощью команд движения и сжигания топлива"""
    start_position = Vector(0, 0)
    velocity = Vector(10, 0)
    expected_position = Vector(10, 0)

    fuel_level = 100
    fuel_consumption = 10
    # 10 топлива * (10, 0)
    expected_fuel_level = 0

    movable_fuel_consumer = make_movable_fuel_consumer(start_position, velocity, fuel_level, fuel_consumption)
    command = MoveWithFuelCommand(movable_fuel_consumer)
    command.execute()

    assert movable_fuel_consumer.get_position() == expected_position
    assert movable_fuel_consumer.get_fuel_level() == expected_fuel_level

def test_macro_command_with_invalid_params():
    """Тест работы макро-команды с вызовом ошибки"""
    start_position = Vector(0, 0)
    velocity = Vector(10, 0)

    fuel_level = 10
    fuel_consumption = 100

    movable_fuel_consumer = make_movable_fuel_consumer(start_position, velocity, fuel_level, fuel_consumption)
    command = MoveWithFuelCommand(movable_fuel_consumer)
    with pytest.raises(CommandException) as e:
        command.execute()
