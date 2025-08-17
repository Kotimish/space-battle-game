from src.commands.log_exception_command import LogExceptionCommand
from src.commands.move import MoveCommand
from src.exceptions.move import UnchangeablePositionError
from src.models.vector import Vector
from tests.test_move import make_movable_object


def test_log_exception_command(caplog):
    """Тест команды для записи информации о выброшенном исключении в лог"""
    start_position = Vector(12, 5)
    velocity = Vector(-7, 3)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    exception = UnchangeablePositionError('The object has not changed position.')
    expected_message = f'Command \"MoveCommand\" failed: {exception}'

    log_cmd = LogExceptionCommand(command, exception)
    log_cmd.execute()

    # Проверяем, что сообщение появилось в логах
    assert expected_message in caplog.text
