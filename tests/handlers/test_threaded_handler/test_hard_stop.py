import threading
from unittest.mock import Mock

from src.commands.control.hard_stop_command import HardStopCommand
from src.commands.control.start_command_handler import StartCommandHandler
from src.commands.move import MoveCommand
from src.handlers.threaded_command_handler import ThreadedCommandHandler
from src.models.vector import Vector
from tests.factories import make_movable_object


def test_hard_stop(event_loop: ThreadedCommandHandler) -> None:
    """
    Тестирование жесткой остановки выполнения event-loop в потоке.
    После выполнения HardStopCommand следующие команды в очереди не будут выполнены
    """
    start_position = Vector(12, 6)
    velocity = Vector(-6, -3)
    # Предполагается только одно применение velocity к start_position из-за жесткой остановки
    end_position = Vector(6, 3)
    movable_object = make_movable_object(start_position, velocity)
    # Команда-пустышка, сигнализирующая о завершении через событие
    event = threading.Event()
    post_command = Mock()
    post_command.execute = lambda: event.set()
    event_loop.add_after_hook(post_command)
    # Заполнение очереди
    commands = [
        MoveCommand(movable_object),
        HardStopCommand(event_loop),
        MoveCommand(movable_object),
    ]
    for command in commands:
        event_loop.enqueue_command(command)

    StartCommandHandler(event_loop).execute()
    # Ожидание завершение через команду-пустышку
    event.wait()
    assert movable_object.get_position() == end_position
