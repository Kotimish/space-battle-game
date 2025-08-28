from src.exceptions.base_exception import BaseGameException


class FuelException(BaseGameException):
    """Базовое исключение для ошибок работы с топливом."""


class UndefinedFuelLevelError(FuelException):
    """Объект не имеет уровня топлива"""


class UndefinedFuelConsumptionError(FuelException):
    """Объект не имеет определенного уровня потребления топлива"""

