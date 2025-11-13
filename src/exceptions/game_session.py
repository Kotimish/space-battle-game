from src.exceptions.base_exception import BaseGameException


class GameSessionException(BaseGameException):
    """Базовое исключение для игровых сессий."""


class GameNotFoundError(GameSessionException):
    """Ошибка возникает, когда игровая сессия с указанным идентификатором не существует или не найдена."""


class GameAlreadyExistsError(GameSessionException):
    """Ошибка возникает, когда игровая сессия с указанным идентификатором уже существует."""


class InvalidGameIdError(GameSessionException):
    """Некорректный формат идентификатора игровой сессии."""
