from abc import ABC, abstractmethod

from src.domain.interfaces.movable_object import IMovableObject
from src.domain.interfaces.weapon_object import IWeaponObject


class IShootableObject(IMovableObject, ABC):
    """Интерфейс для объектов, способных стрелять."""

    @abstractmethod
    def get_weapon(self) -> 'IWeaponObject':
        """Получить оружие объекта."""
        raise NotImplementedError
