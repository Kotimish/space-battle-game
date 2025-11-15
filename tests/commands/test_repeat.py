from src.application.commands.move import MoveCommand
from src.application.commands.repeat import RepeatCommand
from src.domain.models.vector import Vector
from tests.helpers.factories import make_movable_object


def test_repeat_command():
    """Тест повтора команды обработчиком исключений на примере команды движения"""
    start_position = Vector(12, 5)
    velocity = Vector(-7, 3)
    end_position = Vector(5, 8)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    repeat_command = RepeatCommand(command)
    repeat_command.execute()

    assert movable_object.get_position() == end_position
