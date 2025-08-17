from queue import Queue

from src.exceptions.exception_handler import ExceptionHandler
from src.interfaces.base_command import BaseCommand


class CommandHandler:
    """Класс реализации event loop для команд"""
    def __init__(self, queue: Queue[BaseCommand], exception_handler: ExceptionHandler):
        self._queue: Queue[BaseCommand] = queue
        self._exception_handler = exception_handler

    def enqueue_command(self, cmd: BaseCommand):
        self._queue.put(cmd)

    def dequeue_command(self):
        return self._queue.get()

    def run(self):
        while not self._queue.empty():
            cmd = self.dequeue_command()
            try:
                cmd.execute()
            except Exception as exception:
                handler = self._exception_handler.handle(cmd, exception)
                self.enqueue_command(handler)
