import pytest

from src.application.commands.macro.rotate_with_velocity import RotateWithVelocityCommand
from src.domain.models.angle import Angle
from src.domain.models.vector import Vector
from src.domain.exceptions.command import MacroCommandException
from tests.factories import make_rotatable_object, make_movable_with_velocity_object


@pytest.mark.parametrize(
    'start_velocity, angular_velocity, expected_velocity',
    [
        (Vector(10,0), Angle(2, 8), Vector(0, 10)),
        (Vector(10,0), Angle(4, 8), Vector(-10, 0)),
        (Vector(10,0), Angle(6, 8), Vector(0, -10)),
        # (Vector(10,0), Angle(8, 8), Vector(10, 0)),
        # 'Некрасивые' углы
        (Vector(10, 0), Angle(1, 8), Vector(7, 7)),
        (Vector(0, 10), Angle(1, 8), Vector(-7, 7)),
    ]
)
def test_rotate_with_velocity_with_valid_params(
        start_velocity: Vector,
        angular_velocity: Angle,
        expected_velocity: Vector
):
    """Тест макро-команды поворота и последующего изменения мгновенной скорости"""
    position = Vector(0, 0)
    angle = Angle(0, 8)
    expected_angle = angular_velocity

    movable_object = make_movable_with_velocity_object(position, start_velocity)
    rotatable_object = make_rotatable_object(angle, angular_velocity)
    command = RotateWithVelocityCommand(movable_object, rotatable_object)
    command.execute()

    assert rotatable_object.get_angle() == expected_angle
    assert movable_object.get_velocity() == expected_velocity


@pytest.mark.parametrize(
    'start_velocity, angular_velocity',
    [
        (Vector(0,0), Angle(8, 8),),
        (Vector(10,0), Angle(0, 0),),
        (Vector(10,0), Angle(8, 8),),
    ]
)
def test_rotate_with_velocity_with_invalid_params(
        start_velocity: Vector,
        angular_velocity: Angle,
):
    """
    Тест макро-команды поворота и последующего изменения мгновенной скорости
    при некорректных параметрах
    """
    position = Vector(0, 0)
    angle = Angle(0, 8)

    movable_object = make_movable_with_velocity_object(position, start_velocity)
    rotatable_object = make_rotatable_object(angle, angular_velocity)
    command = RotateWithVelocityCommand(movable_object, rotatable_object)
    with pytest.raises(MacroCommandException) as e:
        command.execute()