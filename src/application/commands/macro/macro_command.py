from src.domain.exceptions.command import MacroCommandException
from src.domain.interfaces.base_command import BaseCommand


class MacroCommand(BaseCommand):
    """Простейшая макро-команда для запуска нескольких команд"""
    def __init__(self, commands: list[BaseCommand] = None):
        self._commands = commands if commands is not None else []

    def execute(self) -> None:
        for command in self._commands:
            try:
                command.execute()
            except Exception as exception:
                raise MacroCommandException(f'Error while executing MacroCommand: {exception}') from exception
