import pytest

from src.application.commands.rotate import RotateCommand
from src.domain.exceptions.rotate import UndefinedAngleError, UndefinedAngularVelocityError, UnchangeableAngleError
from src.domain.models.angle import Angle
from tests.helpers.factories import make_rotatable_object


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
