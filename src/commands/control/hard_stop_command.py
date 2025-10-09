from src.handlers.threaded_command_handler import ThreadedCommandHandler
from src.interfaces.base_command import BaseCommand


class HardStopCommand(BaseCommand):
    """Команда остановки цикла выполнения команд не дожидаясь их полного завершения"""
    def __init__(self, handler: ThreadedCommandHandler):
        self._handler = handler

    def execute(self) -> None:
        self._handler.hard_stop()
