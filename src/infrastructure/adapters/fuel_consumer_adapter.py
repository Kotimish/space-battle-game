from src.domain.exceptions.fuel_command import UndefinedFuelLevelError, UndefinedFuelConsumptionError
from src.domain.interfaces.fuel_consumer_object import IFuelConsumerObject
from src.domain.interfaces.uobject import UObject


class FuelConsumerAdapter(IFuelConsumerObject):
    """Адаптер для объектов, которые потребляют топливо"""
    def __init__(self, obj: UObject):
        self.obj = obj

    def get_fuel_level(self) -> int:
        if not self.obj.check_property('fuel_level'):
            raise UndefinedFuelLevelError(f"Object has no attribute 'fuel_level'.")
        fuel_level = self.obj.get_property('fuel_level')
        if fuel_level is None:
            raise UndefinedFuelLevelError(f"Object has no attribute 'fuel_level'.")
        return fuel_level

    def set_fuel_level(self, fuel_level: int):
        self.obj.set_property('fuel_level', fuel_level)

    def get_fuel_consumption(self):
        if not self.obj.check_property('fuel_consumption'):
            raise UndefinedFuelConsumptionError(f"Object has no attribute 'fuel_consumption'.")
        fuel_consumption = self.obj.get_property('fuel_consumption')
        if fuel_consumption is None:
            raise UndefinedFuelConsumptionError(f"Object has no attribute 'fuel_consumption'.")
        return fuel_consumption
