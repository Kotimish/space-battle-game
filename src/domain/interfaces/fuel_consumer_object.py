from abc import ABC, abstractmethod


class IFuelConsumerObject(ABC):
    """Интерфейс для объектов, которые потребляют топливо"""
    @abstractmethod
    def get_fuel_level(self) -> int:
        """Узнать уровень топлива у объекта"""
        raise NotImplementedError

    @abstractmethod
    def set_fuel_level(self, fuel_level: int):
        """Задать уровень топлива объекту"""
        raise NotImplementedError

    def get_fuel_consumption(self):
        """Возвращает расход топлива для выполнения действия"""
        raise NotImplementedError
