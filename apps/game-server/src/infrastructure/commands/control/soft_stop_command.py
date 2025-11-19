from src.infrastructure.handlers.threaded_command_handler import ThreadedCommandHandler
from src.domain.interfaces.base_command import BaseCommand


class SoftStopCommand(BaseCommand):
    """Команда остановки цикла выполнения команд только после завершения их выполнения"""
    def __init__(self, handler: ThreadedCommandHandler):
        self._handler = handler

    def execute(self) -> None:
        self._handler.soft_stop()
