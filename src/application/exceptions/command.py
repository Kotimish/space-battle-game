from src.domain.exceptions.base_exception import BaseGameException


class CommandException(BaseGameException):
    """Базовое исключение для ошибок работы команд прикладного слоя."""


class CommandNotFoundError(CommandException):
    """Ошибка возникает, когда указанная команда не существует или не найдена."""
