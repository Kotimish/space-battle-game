import threading
from unittest.mock import Mock

from src.application.commands.move import MoveCommand
from src.domain.models.vector import Vector
from src.infrastructure.commands.control.hard_stop_command import HardStopCommand
from src.infrastructure.commands.control.move_to_command import MoveToCommand
from src.infrastructure.commands.control.start_command_handler import RunCommand
from src.infrastructure.dependencies.ioc import IoC
from src.infrastructure.handlers.threaded_command_handler import ThreadedCommandHandler
from tests.helpers.factories import make_movable_object


def test_move_to() -> None:
    """
    Тестирование команды перенаправления выполнения команд в другую очередь.
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

    # Создание двух обработчиков очередей команд
    event_loop_1 = IoC[ThreadedCommandHandler].resolve("ThreadedCommandHandler")
    event_loop_2 = IoC[ThreadedCommandHandler].resolve("ThreadedCommandHandler")


    event_loop_2.add_after_hook(post_command)
    # Заполнение очереди
    commands = [
        # Команда перенаправления
        MoveToCommand(event_loop_2._queue),
        MoveCommand(movable_object),
        # Команда остановки, которую ожидает event.wait()
        HardStopCommand(),
        MoveCommand(movable_object),
    ]
    for command in commands:
        event_loop_1.enqueue_command(command)

    # Запускаем целевую очередь раньше перенаправляемой
    event_loop_2.start()
    event_loop_1.start()
    # Ожидание явного завершения второй очереди, куда перенаправляется поток с командой жесткой остановки
    event.wait()
    assert movable_object.get_position() == end_position
    # После успешной проверки явно останавливаем оставшийся поток
    event_loop_1.enqueue_command(HardStopCommand())



def test_return_normal_state() -> None:
    """
    Тестирование команды перенаправления выполнения команд в другую очередь и возврата обычного режима.
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

    # Создание двух обработчиков очередей команд
    event_loop_1 = IoC[ThreadedCommandHandler].resolve("ThreadedCommandHandler")
    event_loop_2 = IoC[ThreadedCommandHandler].resolve("ThreadedCommandHandler")


    event_loop_1.add_after_hook(post_command)
    # Заполнение очереди
    commands = [
        # Перенаправление потока команд
        MoveToCommand(event_loop_2._queue),
        # Возврат обычного состояния обработки
        RunCommand(),
        MoveCommand(movable_object),
        # Команда остановки, которую ожидает event.wait()
        HardStopCommand(),
        MoveCommand(movable_object),
    ]
    for command in commands:
        event_loop_1.enqueue_command(command)

    # Запускаем целевую очередь раньше перенаправляемой
    event_loop_2.start()
    event_loop_1.start()
    # Ожидание явного завершения первой очереди, куда возвращается
    event.wait()
    assert movable_object.get_position() == end_position
    # После успешной проверки явно останавливаем оставшийся поток
    event_loop_2.enqueue_command(HardStopCommand())
