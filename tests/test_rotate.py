import pytest

from src.adapters.rotatable_adapter import RotatableObjectAdapter
from src.commands.rotate import RotateCommand
from src.exceptions.rotate import UndefinedAngleError, UndefinedAngularVelocityError, UnchangeableAngleError
from src.models.angle import Angle
from tests.mock_object import MockUObject


def make_rotatable_object(angle: Angle, angular_velocity: Angle) -> RotatableObjectAdapter:
    data = {"angle": angle, "angular_velocity": angular_velocity}
    mock_object = MockUObject(data)
    rotatable_object = RotatableObjectAdapter(mock_object)
    return rotatable_object


def test_rotate_with_valid_params():
    """
    Тест вращения объекта от 45 градусов до 180 градусов с шагом в 135 градусов
    """
    start_angle = Angle(1, 8)
    angular_velocity = Angle(3, 8)
    end_angle = Angle(4, 8)

    rotate_object = make_rotatable_object(start_angle, angular_velocity)
    rotate = RotateCommand(rotate_object)
    rotate.execute()

    print(rotate_object.get_angle())
    print(end_angle)
    assert rotate_object.get_angle() == end_angle


def test_rotate_with_invalid_angle():
    """
    Тест объекта, у которого невозможно прочитать угол
    """
    start_angle = None
    angular_velocity = Angle(3, 8)

    rotate_object = make_rotatable_object(start_angle, angular_velocity)
    rotate = RotateCommand(rotate_object)
    with pytest.raises(UndefinedAngleError):
        rotate.execute()


def test_rotate_with_invalid_angular_velocity():
    """
    Тест объекта, у которого невозможно прочитать значение угловой скорости
    """
    start_angle = Angle(1, 8)
    angular_velocity = None

    rotate_object = make_rotatable_object(start_angle, angular_velocity)
    rotate = RotateCommand(rotate_object)
    with pytest.raises(UndefinedAngularVelocityError):
        rotate.execute()


def test_unchangeable_angle():
    """
    Тест объекта, у которого невозможно изменить положение угол
    """
    start_angle = Angle(1, 8)
    angular_velocity = Angle(0, 8)

    rotate_object = make_rotatable_object(start_angle, angular_velocity)
    rotate = RotateCommand(rotate_object)
    with pytest.raises(UnchangeableAngleError):
        rotate.execute()
