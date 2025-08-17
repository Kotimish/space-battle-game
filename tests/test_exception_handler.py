from queue import Queue


from src.commands.command_handler import CommandHandler
from src.commands.log_exception_command import LogExceptionCommand
from src.commands.move import MoveCommand
from src.exceptions.exception_handler import ExceptionHandler
from src.exceptions.move import UnchangeablePositionError
from src.models.vector import Vector
from tests.test_move import make_movable_object


def test_success_repeat_command():
    """Тест повтора команды обработчиком исключений на примере команды движения"""
    start_position = Vector(12, 5)
    velocity = Vector(-7, 3)
    end_position = Vector(5, 8)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)

    exception_handler = ExceptionHandler()
    handler = exception_handler.handle(command, UnchangeablePositionError())
    handler.execute()

    assert movable_object.get_position() == end_position


def test_fail_repeat_command(caplog):
    """Тест повтора команды обработчиком исключений на примере команды движения"""
    start_position = Vector(12, 5)
    velocity = Vector(0, 0)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    # Обработчик ошибок
    exception = UnchangeablePositionError('The object has not changed position.')
    inner_expected_message = f'RepeatCommand for command MoveCommand'
    expected_message = f'Command \"{inner_expected_message}\" failed: {exception}'
    exception_handler = ExceptionHandler()
    # Обработчик команд
    command_handler = CommandHandler(Queue(), exception_handler)
    command_handler.enqueue_command(command)
    command_handler.run()

    # Проверяем, что сообщение появилось в логах
    print(expected_message)
    print(caplog.text)
    assert expected_message in caplog.text


def test_log_exception_command(caplog):
    """Тест команды для записи информации о выброшенном исключении в лог"""
    start_position = Vector(12, 5)
    velocity = Vector(-7, 3)
    end_position = Vector(5, 8)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    exception = UnchangeablePositionError('The object has not changed position.')
    expected_message = f'Command \"MoveCommand\" failed: {exception}'

    log_cmd = LogExceptionCommand(command, exception)
    log_cmd.execute()

    # Проверяем, что сообщение появилось в логах
    assert expected_message in caplog.text
