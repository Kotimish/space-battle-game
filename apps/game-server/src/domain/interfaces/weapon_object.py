from abc import ABC, abstractmethod


class IWeaponObject(ABC):
    """Интерфейс для объектов, представляющих оружие"""

    @abstractmethod
    def get_damage(self) -> int:
        """Получить урон оружия"""
        raise NotImplementedError

    @abstractmethod
    def get_range(self) -> int:
        """Получить дальность оружия"""
        raise NotImplementedError

    @abstractmethod
    def can_shoot(self) -> bool:
        """Проверить, может ли оружие выполнить выстрел"""
        raise NotImplementedError