from src.application.commands.move import MoveCommand
from src.application.commands.repeat import RepeatCommand, SecondRepeatCommand
from src.domain.exceptions.move import UnchangeablePositionError
from src.domain.models.vector import Vector
from src.infrastructure.handlers.command_handler import CommandHandler
from src.infrastructure.handlers.exception_handler import ExceptionHandler
from tests.helpers.factories import make_movable_object


def test_success_repeat_command():
    """
    Тест успешного повтора команды обработчиком исключений на примере команды движения
    с использованием обработчика ошибок
    """
    start_position = Vector(12, 5)
    velocity = Vector(-7, 3)
    end_position = Vector(5, 8)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    # Обработчик ошибок
    exception_handler = ExceptionHandler()
    handler = exception_handler.handle(command, UnchangeablePositionError())
    handler.execute()

    assert movable_object.get_position() == end_position


def test_fail_repeat_command(caplog):
    """
    Тест неудачного повтора команды обработчиком исключений
    на примере команды движения с выводом сообщения в лог
    с использованием обработчика ошибок и обработчика команд
    """
    start_position = Vector(12, 5)
    velocity = Vector(0, 0)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    # Ожидаемое сообщение об ошибке
    exception = UnchangeablePositionError('The object has not changed position.')
    inner_expected_message = f'RepeatCommand for command MoveCommand'
    expected_message = f'Command \"{inner_expected_message}\" failed: {exception}'
    # Обработчик ошибок
    exception_handler = ExceptionHandler()
    # Обработчик команд
    command_handler = CommandHandler(None, exception_handler)
    command_handler.enqueue_command(command)
    command_handler.start()

    # Проверяем, что сообщение появилось в логах
    assert expected_message in caplog.text


def test_two_repeats_command(caplog):
    """
    Тест стратегии повтора два раза команды обработчиком исключений на примере команды движения
    с использованием обработчика ошибок и обработчика команд
    """
    start_position = Vector(12, 5)
    velocity = Vector(0, 0)

    movable_object = make_movable_object(start_position, velocity)
    command = MoveCommand(movable_object)
    # Ожидаемое сообщение об ошибке
    exception = UnchangeablePositionError('The object has not changed position.')
    inner_expected_message = f'SecondRepeatCommand for command MoveCommand'
    expected_message = f'Command \"{inner_expected_message}\" failed: {exception}'
    # Обработчик ошибок
    exception_handler = ExceptionHandler()
    # Явно регистрируем команду стратегии двойного повтора для одинарного
    exception_handler.register_default_handler_for_command(
        RepeatCommand,
        lambda cmd, exc: SecondRepeatCommand(cmd.command_to_retry)
    )
    # Обработчик команд
    command_handler = CommandHandler(None, exception_handler)
    command_handler.enqueue_command(command)
    command_handler.start()

    # Проверяем, что сообщение появилось в логах
    assert expected_message in caplog.text
