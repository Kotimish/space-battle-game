from src.exceptions.base_exception import BaseGameException


class CommandException(BaseGameException):
    """Базовое исключение для ошибок работы команд."""


class CommandNotFoundError(CommandException):
    """Ошибка возникает, когда указанная команда не существует или не найдена."""
