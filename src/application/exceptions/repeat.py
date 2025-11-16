from src.domain.exceptions.base_exception import BaseGameException


class RepeatException(BaseGameException):
    """Базовое исключение для ошибок повторного выполнения команд."""
