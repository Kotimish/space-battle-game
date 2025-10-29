from src.exceptions.base_exception import BaseGameException


class GameObjectException(BaseGameException):
    """Базовое исключение для игровых объектов."""


class ObjectNotFoundError(GameObjectException):
    """Ошибка возникает, когда указанный игровой объект не существует или не найден."""
