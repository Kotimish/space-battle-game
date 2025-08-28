from typing import Callable

import src.handlers.exception_mapping as exc_map
from src.interfaces.base_command import BaseCommand

# Оптимизация типов
CommandType = type[BaseCommand]
ExceptionType = type[Exception]
HandlerType = Callable[[BaseCommand, Exception], BaseCommand]

class ExceptionHandler:
    """Обработчик исключений"""
    def __init__(
            self,
            commands: dict[CommandType, dict[ExceptionType, HandlerType]]=None,
            default_commands: dict[CommandType, HandlerType]=None,
            default_exceptions: dict[ExceptionType, HandlerType]=None,
            default_handler: HandlerType = None
    ):
        self._handlers = commands or exc_map.DEFAULT_HANDLERS
        self._default_command_handlers = default_commands or exc_map.DEFAULT_COMMANDS
        self._default_exception_handlers = default_exceptions or exc_map.DEFAULT_EXCEPTIONS
        self._default_handler = default_handler or exc_map.DEFAULT_HANDLER

    def register_handler(self, cmd_type: CommandType, exc_type: ExceptionType, handler: HandlerType):
        """Регистрация нового обработчика на основе типа команды и типа исключения"""
        self._handlers[cmd_type][exc_type] = handler

    def register_default_handler_for_command(self, cmd_type: CommandType, handler: HandlerType):
        """Регистрация нового обработчика на основе типа команды для любого типа исключения"""
        self._default_command_handlers[cmd_type] = handler

    def register_default_handler_for_exception(self, exc_type: ExceptionType, handler: HandlerType):
        """Регистрация нового обработчика на основе типа исключения для любого типа команд"""
        self._default_exception_handlers[exc_type] = handler

    def register_default_handler(self, handler: HandlerType):
        """Регистрация дефолтного обработчика"""
        self._default_handler = handler

    def handle(self, cmd: BaseCommand, exception: Exception) -> BaseCommand:
        """Получение команды-обработчика на основе команды с исключением"""
        cmd_type = type(cmd)
        exc_type = type(exception)
        # Поиск обработчика
        if cmd_type in self._handlers and exc_type in self._handlers[cmd_type]:
            return self._handlers[cmd_type][exc_type](cmd, exception)
        # Ищем по типу команды, если отсутствует исключение
        if cmd_type in self._default_command_handlers:
            return self._default_command_handlers[cmd_type](cmd, exception)
        # Ищем по типу исключения, если отсутствует команда
        if exc_type in self._default_exception_handlers:
            return self._default_exception_handlers[exc_type](cmd, exception)
        # Иначе возвращаем дефолтный обработчик
        return self._default_handler(cmd, exception)
