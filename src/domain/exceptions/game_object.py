from src.domain.exceptions.base_exception import BaseGameException


class GameObjectException(BaseGameException):
    """Базовое исключение для игровых объектов."""


class ObjectNotFoundError(GameObjectException):
    """Ошибка возникает, когда указанный игровой объект не существует или не найден."""


class ObjectAlreadyExistsError(BaseGameException):
    """Ошибка возникает, когда игровая сессия с указанным идентификатором уже существует."""
