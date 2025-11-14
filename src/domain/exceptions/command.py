from src.domain.exceptions.base_exception import BaseGameException


class CommandException(BaseGameException):
    """Базовое исключение для ошибок работы команд доменного слоя."""


class MacroCommandException(BaseGameException):
    """Базовое исключение для ошибок работы макро-команд доменного слоя."""


