from queue import Queue

from src.handlers.exception_handler import ExceptionHandler
from src.interfaces.base_command import BaseCommand
from src.interfaces.command_handler import ICommandHandler


class CommandHandler(ICommandHandler):
    """Класс реализации блокирующего event-loop для команд"""

    def __init__(self, queue: Queue[BaseCommand] = None, exception_handler: ExceptionHandler = None):
        self._queue = queue or Queue()
        self._exception_handler = exception_handler or ExceptionHandler()

    def enqueue_command(self, cmd: BaseCommand) -> None:
        """Добавление новой команды в конец очереди"""
        self._queue.put(cmd)

    def dequeue_command(self) -> BaseCommand:
        """Получение первой команды из очереди"""
        return self._queue.get()

    def _run(self) -> None:
        """Выполнение всех команд из очереди"""
        while not self._queue.empty():
            command = self.dequeue_command()
            try:
                command.execute()
            except Exception as exception:
                handler = self._exception_handler.handle(command, exception)
                self.enqueue_command(handler)

    def start(self) -> None:
        self._run()

    def stop(self) -> None:
        # Ничего не делаем — обработчик и так завершится после выполнения всех команд
        pass
