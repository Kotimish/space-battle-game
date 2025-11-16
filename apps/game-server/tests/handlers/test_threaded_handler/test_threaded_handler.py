import threading
from unittest.mock import Mock

from src.infrastructure.commands.control.hard_stop_command import HardStopCommand
from src.infrastructure.commands.control.start_command_handler import StartCommandHandler
from src.infrastructure.handlers.threaded_command_handler import ThreadedCommandHandler


def test_threaded_command_handler(event_loop: ThreadedCommandHandler):
    """Тестирования запуска неблокирующего event-loop в потоке"""
    # Команда-пустышка, сигнализирующая о завершении через событие
    event = threading.Event()
    mock_command = Mock()
    mock_command.execute = lambda: event.set()
    # Заполнение очереди
    commands = [
        mock_command
    ]
    for command in commands:
        event_loop.enqueue_command(command)

    StartCommandHandler(event_loop).execute()
    # Ожидание завершение через команду-пустышку
    event.wait()
    # Для завершения фоновой задачи
    event_loop.enqueue_command(HardStopCommand(event_loop))
