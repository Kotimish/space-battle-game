from src.domain.exceptions.base_exception import BaseGameException


class RotateException(BaseGameException):
    """Базовое исключение для ошибок поворачиваемых объектов."""


class UndefinedAngleError(RotateException):
    """Объект не имеет определяемого угла"""


class UndefinedAngularVelocityError(RotateException):
    """Объект не имеет определяемой угловой скорости"""


class UnchangeableAngleError(RotateException):
    """Угол объекта не может быть изменен"""
