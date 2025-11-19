from src.domain.interfaces.shootable_object import IShootableObject
from src.domain.interfaces.uobject import UObject
from src.infrastructure.adapters.movable_adapter import MovableObjectAdapter
from src.infrastructure.adapters.weapon_object_adapter import WeaponObjectAdapter

class ShootableObjectAdapter(MovableObjectAdapter, IShootableObject):
    """
    Адаптер, позволяющий UObject реализовать интерфейс IShootableObject.
    Предполагает, что UObject может быть адаптирован к IWeaponObject.
    """

    def __init__(self, obj: UObject):
        super().__init__(obj)
        # Вложенный адаптер для оружия
        self._weapon_adapter = WeaponObjectAdapter(obj)

    def get_weapon(self):
        return self._weapon_adapter