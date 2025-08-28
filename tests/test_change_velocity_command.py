from types import NoneType

import pytest

from src.adapters.movable_with_velocity_adapter import MovableWithVelocityAdapter
from src.commands.change_velocity_command import ChangeVelocityCommand
from src.models.angle import Angle
from src.models.vector import Vector
from tests.mock_object import MockUObject
from tests.test_rotate import make_rotatable_object


def make_movable_object(position: Vector, velocity: Vector) -> MovableWithVelocityAdapter:
    data = {"position": position, "velocity": velocity}
    mock_object = MockUObject(data)
    movable_object = MovableWithVelocityAdapter(mock_object)
    return movable_object


@pytest.mark.parametrize(
    'start_velocity, angular_velocity, expected_velocity',
    [
        (Vector(10,0), Angle(2, 8), Vector(0, 10)),
        (Vector(10,0), Angle(4, 8), Vector(-10, 0)),
        (Vector(10,0), Angle(6, 8), Vector(0, -10)),
        (Vector(10,0), Angle(8, 8), Vector(10, 0)),
        # 'Некрасивые' углы
        (Vector(10, 0), Angle(1, 8), Vector(7, 7)),
        (Vector(0, 10), Angle(1, 8), Vector(-7, 7)),
    ]
)
def test_change_velocity_with_valid_params(start_velocity: Vector, angular_velocity: Angle, expected_velocity: Vector):
    """Тест объекта на изменение вектора скорости при повороте"""
    position = Vector(0, 0)
    angle = Angle(0, 8)

    movable_object = make_movable_object(position, start_velocity)
    rotatable_object = make_rotatable_object(angle, angular_velocity)
    command = ChangeVelocityCommand(movable_object, rotatable_object)
    command.execute()

    assert movable_object.get_velocity() == expected_velocity


@pytest.mark.parametrize(
    'angular_velocity',
    [
        Angle(2, 8),
        Angle(6, 8),
    ]
)
def test_change_velocity_with_zero_velocity(angular_velocity: Angle):
    """
    Тест объекта на изменение вектора скорости
    при повороте при нулевом векторе
    """
    position = Vector(0, 0)
    start_velocity = Vector(0, 0)
    expected_velocity = Vector(0, 0)

    angle = Angle(0, 8)

    movable_object = make_movable_object(position, start_velocity)
    rotatable_object = make_rotatable_object(angle, angular_velocity)
    command = ChangeVelocityCommand(movable_object, rotatable_object)
    command.execute()

    assert movable_object.get_velocity() == expected_velocity


@pytest.mark.parametrize(
    'velocity',
    [
        Vector(10, 0),
        Vector(0, 10),
    ]
)
def test_change_velocity_with_zero_angular_velocity(velocity: Vector):
    """
    Тест объекта на изменение вектора скорости
    при повороте при нулевой угловой скорости
    """
    position = Vector(0, 0)

    angle = Angle(0, 8)
    angular_velocity = Angle(0, 8)

    movable_object = make_movable_object(position, velocity)
    rotatable_object = make_rotatable_object(angle, angular_velocity)
    command = ChangeVelocityCommand(movable_object, rotatable_object)
    command.execute()

    assert movable_object.get_velocity() == velocity
