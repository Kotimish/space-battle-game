from src.domain.exceptions.base_exception import BaseGameException


class ShootException(BaseGameException):
    """Базовое исключение для ошибок работы со стрельбой."""


class UndefinedHealthPointError(BaseGameException):
    """Объект не имеет определяемого уровня здоровья."""


class UndefinedDamageError(BaseGameException):
    """Объект не имеет определяемого уровня здоровья."""


class UndefinedRangeError(BaseGameException):
    """Объект не имеет определяемой дальности оружием."""


class WeaponCanNotShootError(BaseGameException):
    """Оружие не может выстрелить."""
