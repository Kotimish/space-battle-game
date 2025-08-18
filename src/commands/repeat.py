from src.exceptions.repeat import RepeatException
from src.interfaces.base_command import BaseCommand


class RepeatCommand(BaseCommand):
    """Команда для повтора Команды, выбросившей исключение"""
    def __init__(self, cmd: BaseCommand):
        self.command_to_retry = cmd

    def __str__(self):
        return f'{self.__class__.__name__} for command {self.command_to_retry.__class__.__name__}'

    def execute(self) -> None:
        self.command_to_retry.execute()

class SecondRepeatCommand(RepeatCommand):
    """Команда для второго повтора Команды, выбросившей исключение"""
