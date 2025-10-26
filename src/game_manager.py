import time
import uuid
from threading import Lock

from src.dependencies.ioc import IoC
from src.exceptions import game_manager as exceptions
from src.handlers.threaded_command_handler import ThreadedCommandHandler
from src.interfaces.base_command import BaseCommand
from src.interfaces.command_handler import ICommandHandler


def _generate_session_name() -> str:
    timestamp = int(time.time())
    short_uuid = str(uuid.uuid4())[:8]
    return f"game_{timestamp}_{short_uuid}"


class GameManager:
    """Класс управления жизненным циклом игровых сессий - обработчиков очередей команд"""
    def __init__(self):
        self._handlers: dict[str, ICommandHandler] = {}
        self._lock = Lock()
        self._counter = 0

    def create(self, init_commands: list[BaseCommand] | None = None) -> str:
        """Создание игровой сессии"""
        with self._lock:
            game_id = _generate_session_name()
            if game_id in self._handlers:
                raise exceptions.GameAlreadyExistsError(f"Game '{game_id}' already exists.")
            # Создание скоупа
            scope_name = IoC[BaseCommand].resolve('IoC.Scope.Create', game_id).execute()
            # Создание обработчика
            handler = ThreadedCommandHandler()
            # Явная установка скоупа внутри потока
            handler.add_before_hook(IoC[BaseCommand].resolve('IoC.Scope.Set', scope_name))
            # Регистрируем стандартные зависимости для игровой сессии
            if init_commands is None:
                init_commands = []
            for command in init_commands:
                handler.add_before_hook(command)
            # Регистрируем
            self._handlers[game_id] = handler
        # Запускаем вне блокировки
        handler.start()
        return game_id

    def get(self, game_id: str) -> ICommandHandler:
        """Получение игровой сессии по ID"""
        with self._lock:
            if game_id not in self._handlers:
                raise exceptions.GameNotFoundError(f"Game '{game_id}' does not found.")
            return self._handlers[game_id]

    def stop_game(self, game_id: str) -> None:
        """Остановка игровой сессии по ID"""
        with self._lock:
            if game_id in self._handlers:
                handler = self._handlers.pop(game_id)
                handler.stop()

    def stop_all_games(self) -> None:
        """Остановка всех игровых сессий"""
        with self._lock:
            game_ids = list(self._handlers.keys())
            for game_id in game_ids:
                handler = self._handlers.pop(game_id)
                handler.stop()
