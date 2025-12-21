from queue import Queue, Empty

from src.application.interfaces.states.command_handler_state import ICommandHandlerState
from src.domain.interfaces.base_command import BaseCommand
from src.infrastructure.commands.control.hard_stop_command import HardStopCommand
from src.infrastructure.commands.control.move_to_command import MoveToCommand
from src.infrastructure.commands.control.soft_stop_command import SoftStopCommand
from src.infrastructure.commands.control.start_command_handler import RunCommand
from src.infrastructure.handlers.exception_handler import ExceptionHandler

HARD_STOP_COMMAND_NAME = HardStopCommand.__name__
SOFT_STOP_COMMAND_NAME = SoftStopCommand.__name__
MOVE_TO_COMMAND_NAME = MoveToCommand.__name__
RUN_COMMAND_NAME = RunCommand.__name__


class NormalState(ICommandHandlerState):
    """Стандартное состояние обработчика команд из очереди"""

    def __init__(self):
        self.states = {
            HARD_STOP_COMMAND_NAME: lambda  *args, **kwargs: None,
            SOFT_STOP_COMMAND_NAME: lambda  *args, **kwargs: SoftStopState(),
            MOVE_TO_COMMAND_NAME: lambda command, *args, **kwargs: MoveToState(target_queue=command.target_queue),
        }
        self.timeout = 0.1

    def handle(
            self,
            queue: Queue[BaseCommand],
            exception_handler: ExceptionHandler
    ) -> ICommandHandlerState | None:
        try:
            command = queue.get(timeout=self.timeout)
        except Empty:
            # Возвращает себя для повторного вызова и проверки очереди
            return self
        try:
            command.execute()
        except Exception as exception:
            handler = exception_handler.handle(command, exception)
            queue.put(handler)

        command_name = command.__class__.__name__
        if command_name in self.states:
            strategy = self.states[command_name](command)
        else:
            strategy = self

        return strategy


class SoftStopState(ICommandHandlerState):
    """Состояние мягкой остановки с остановкой после обработки всех команд"""

    def __init__(self):
        self.states = {
            HARD_STOP_COMMAND_NAME: lambda: None,
            RUN_COMMAND_NAME: NormalState,
        }
        self.timeout = 0.1


    def handle(
            self,
            queue: Queue[BaseCommand],
            exception_handler: ExceptionHandler
    ) -> ICommandHandlerState | None:

        try:
            command = queue.get(timeout=self.timeout)
        except Empty:
            # Явная остановка
            return None
        try:
            command.execute()
        except Exception as e:
            handler = exception_handler.handle(command, e)
            queue.put(handler)

        command_name = command.__class__.__name__
        if command_name in self.states:
            strategy = self.states[command_name]()
        else:
            strategy = self

        return strategy


class MoveToState(ICommandHandlerState):
    """Состояние перенаправления выполнения команд из очереди в другую очередь"""
    def __init__(self, target_queue: Queue[BaseCommand]):
        self.states = {
            HARD_STOP_COMMAND_NAME: lambda: None,
            SOFT_STOP_COMMAND_NAME: SoftStopState,
            RUN_COMMAND_NAME: NormalState,
        }
        self.target_queue = target_queue
        self.timeout = 0.1

    def handle(
        self,
        queue: Queue[BaseCommand],
        exception_handler: ExceptionHandler
    ) -> ICommandHandlerState | None:
        try:
            command = queue.get(timeout=self.timeout)
        except Empty:
            # Возвращает себя для повторного вызова и проверки очереди
            return self
        try:
            self.target_queue.put(command)
        except Exception as exception:
            handler = exception_handler.handle(command, exception)
            queue.put(handler)

        command_name = command.__class__.__name__
        if command_name in self.states:
            strategy = self.states[command_name]()
        else:
            strategy = self

        return strategy
