import logging

from src.domain.interfaces.base_command import BaseCommand


class LogExceptionCommand(BaseCommand):
    """Команда для записи информации о выброшенном исключении в лог"""
    def __init__(self, cmd: BaseCommand, exception: Exception):
        self._cmd = cmd
        self._exception = exception

    def execute(self) -> None:
        logging.error(f'Command \"{self._cmd}\" failed: {self._exception}')
