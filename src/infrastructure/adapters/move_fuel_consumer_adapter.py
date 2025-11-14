from src.infrastructure.adapters.fuel_consumer_adapter import FuelConsumerAdapter
from src.infrastructure.adapters.movable_adapter import MovableObjectAdapter
from src.domain.exceptions.fuel_command import UndefinedFuelConsumptionError
from src.domain.interfaces.move_fuel_consumer import IMoveFuelConsumer
from src.domain.interfaces.uobject import UObject


class MoveFuelConsumer(MovableObjectAdapter, FuelConsumerAdapter, IMoveFuelConsumer):
    """Адаптер для движимого объекта с потреблением топлива"""
    def __init__(self, obj: UObject):
        super().__init__(obj)
        self.obj = obj

    def get_fuel_consumption(self):
        if not self.obj.check_property('fuel_consumption'):
            raise UndefinedFuelConsumptionError(f"Object has no attribute 'fuel_consumption'.")
        fuel_consumption = self.obj.get_property('fuel_consumption')
        if fuel_consumption is None:
            raise UndefinedFuelConsumptionError(f"Object has no attribute 'fuel_consumption'.")
        velocity = self.get_velocity()
        return fuel_consumption * len(velocity)