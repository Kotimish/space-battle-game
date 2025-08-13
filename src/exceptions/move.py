from src.exceptions.base_exception import BaseGameException


class MovementException(BaseGameException):
    """Базовое исключение для ошибок перемещаемых объектов."""


class UndefinedPositionError(MovementException):
    """Объект не имеет определяемой позиции"""


class UndefinedVelocityError(MovementException):
    """Объект не имеет определяемой скорости"""


class UnchangeablePositionError(MovementException):
    """Позиция объекта не может быть изменена"""
