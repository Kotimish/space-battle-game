from src.exceptions.repeat import RepeatException
from src.interfaces.base_command import BaseCommand


class RepeatCommand(BaseCommand):
    """Команда для повтора Команды, выбросившей исключение"""
    def __init__(self, cmd: BaseCommand):
        self._command_to_retry = cmd

    def __str__(self):
        return f'{self.__class__.__name__} for command {self._command_to_retry.__class__.__name__}'

    def execute(self) -> None:
        self._command_to_retry.execute()
