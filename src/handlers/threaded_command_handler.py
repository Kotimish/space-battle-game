import threading
from queue import Queue

from src.handlers.command_handler import CommandHandler
from src.handlers.exception_handler import ExceptionHandler
from src.interfaces.base_command import BaseCommand
from src.interfaces.command_handler import ICommandHandler


class ThreadedCommandHandler(ICommandHandler):
    """Класс реализации неблокирующего event-loop в отдельном потоке для команд"""

    def __init__(self, queue: Queue[BaseCommand] = None, exception_handler: ExceptionHandler = None):
        self._queue: Queue[BaseCommand] = queue or Queue()
        self._exception_handler = exception_handler or ExceptionHandler()
        self._worker: threading.Thread | None = None
        self._running = threading.Event()
        self._soft_stop = False
        # Команды до и после отработки команд в потоке
        self._before_hooks = CommandHandler()
        self._after_hooks = CommandHandler()

    def enqueue_command(self, cmd: BaseCommand) -> None:
        """Добавление новой команды в конец очереди"""
        self._queue.put(cmd)

    def dequeue_command(self) -> BaseCommand:
        """Получение первой команды из очереди"""
        return self._queue.get()

    def _run(self) -> None:
        """Выполнение всех команд из очереди"""
        # Отработка пред-команд
        self._before_hooks.start()
        # Основной цикл выполнения команд
        while (
                self._running.is_set() or
                (not self._queue.empty() and self._soft_stop)
        ):
            command = self.dequeue_command()
            try:
                command.execute()
            except Exception as exception:
                handler = self._exception_handler.handle(command, exception)
                self.enqueue_command(handler)
        # Отработка пост-команд
        self._after_hooks.start()

    def start(self) -> None:
        """Запуск выполнения в потоке"""
        if self._running.is_set():
            raise RuntimeError("ThreadedCommandHandler is already running")
        self._running.set()
        self._worker = threading.Thread(target=self._run)
        self._worker.start()

    def hard_stop(self) -> None:
        self._running.clear()
        if self._worker:
            # ожидание завершения
            self._worker.join()

    def soft_stop(self) -> None:
        self._running.clear()
        self._soft_stop = True
        if self._worker:
            # ожидание завершения
            self._worker.join()

    def add_before_hook(self, command: BaseCommand) -> None:
        self._before_hooks.enqueue_command(command)

    def add_after_hook(self, command: BaseCommand) -> None:
        self._after_hooks.enqueue_command(command)
