import threading
from unittest.mock import Mock

from src.application.commands.move import MoveCommand
from src.domain.models.vector import Vector
from src.infrastructure.commands.control.soft_stop_command import SoftStopCommand
from src.infrastructure.commands.control.start_command_handler import StartCommandHandler
from src.infrastructure.handlers.threaded_command_handler import ThreadedCommandHandler
from tests.factories import make_movable_object


def test_hard_stop(event_loop: ThreadedCommandHandler) -> None:
    """
    Тестирование мягкой остановки выполнения event-loop в потоке.
    После выполнения SoftStopCommand будут выполнены все команды до завершения очереди
    """
    start_position = Vector(12, 6)
    velocity = Vector(-6, -3)
    # Предполагается два применения velocity к start_position из-за мягкой остановки
    end_position = Vector(0, 0)
    movable_object = make_movable_object(start_position, velocity)
    # Команда-пустышка, сигнализирующая о завершении через событие
    event = threading.Event()
    post_command = Mock()
    post_command.execute = lambda: event.set()
    event_loop.add_after_hook(post_command)
    # Заполнение очереди
    commands = [
        MoveCommand(movable_object),
        SoftStopCommand(event_loop),
        MoveCommand(movable_object),
    ]
    for command in commands:
        event_loop.enqueue_command(command)

    StartCommandHandler(event_loop).execute()
    # Ожидание завершение через команду-пустышку
    event.wait()
    assert movable_object.get_position() == end_position
