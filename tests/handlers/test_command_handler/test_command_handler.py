from src.application.commands.move import MoveCommand
from src.domain.models.vector import Vector
from src.infrastructure.commands.control.start_command_handler import StartCommandHandler
from src.infrastructure.handlers.command_handler import CommandHandler
from tests.factories import make_movable_object


def test_command_handler_with_valid_params():
    """Тест работы обработчика команд"""
    movable_object = make_movable_object(Vector(12, 5), Vector(-7, 3))

    command = MoveCommand(movable_object)
    command_handler = CommandHandler()
    command_handler.enqueue_command(command)
    StartCommandHandler(command_handler).execute()

    assert movable_object.get_position() == Vector(5, 8)
