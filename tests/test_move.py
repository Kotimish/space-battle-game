import pytest

from src.adapters.movable_adapter import MovableObjectAdapter
from src.commands.move import MoveCommand
from src.exceptions.move import UndefinedPositionError, UndefinedVelocityError, UnchangeablePositionError
from src.models.vector import Vector
from tests.mock_object import MockUObject


def make_movable_object(position: Vector, velocity: Vector) -> MovableObjectAdapter:
    data = {"position": position, "velocity": velocity}
    mock_object = MockUObject(data)
    movable_object = MovableObjectAdapter(mock_object)
    return movable_object


def test_move_with_valid_params():
    """
    Тест объекта, находящегося в точке (12, 5) и
    движущегося со скоростью (-7, 3)
    движение меняет положение объекта на (5, 8)
    """
    start_position = Vector(12, 5)
    velocity = Vector(-7, 3)
    end_position = Vector(5, 8)

    movable_object = make_movable_object(start_position, velocity)
    move = MoveCommand(movable_object)
    move.execute()

    assert movable_object.get_position() == end_position


def test_move_with_invalid_position():
    """
    Тест объекта, у которого невозможно прочитать положение в пространстве
    """
    start_position = None
    velocity = Vector(-7, 3)

    movable_object = make_movable_object(start_position, velocity)
    move = MoveCommand(movable_object)
    with pytest.raises(UndefinedPositionError):
        move.execute()


def test_move_with_invalid_velocity():
    """
    Тест объекта, у которого невозможно прочитать значение мгновенной скорости
    """
    start_position = Vector(12, 5)
    velocity = None

    movable_object = make_movable_object(start_position, velocity)
    move = MoveCommand(movable_object)
    with pytest.raises(UndefinedVelocityError):
        move.execute()


def test_unchangeable_position():
    """
    Тест объекта, у которого невозможно изменить положение в пространстве
    """
    start_position = Vector(12, 5)
    velocity = Vector(0, 0)

    movable_object = make_movable_object(start_position, velocity)
    move = MoveCommand(movable_object)
    with pytest.raises(UnchangeablePositionError):
        move.execute()
