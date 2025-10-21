from src.interfaces.base_command import BaseCommand
from src.interfaces.command_handler import ICommandHandler


class StartCommandHandler(BaseCommand):
    """Команда запуска event-loop"""
    def __init__(self, command_handler: ICommandHandler):
        self._command_handler = command_handler

    def execute(self) -> None:
        self._command_handler.start()
