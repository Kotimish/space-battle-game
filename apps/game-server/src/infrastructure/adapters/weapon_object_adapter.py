from src.domain.exceptions import shoot as exceptions
from src.domain.interfaces.uobject import UObject
from src.domain.interfaces.weapon_object import IWeaponObject


class WeaponObjectAdapter(IWeaponObject):
    """
    Адаптер, позволяющий UObject реализовать интерфейс IWeaponObject.
    Предполагает, что UObject имеет свойства 'damage', 'range', 'can_shoot'.
    """

    def __init__(self, obj: UObject):
        self.obj = obj

    def get_damage(self) -> int:
        if not self.obj.check_property('damage'):
            raise exceptions.UndefinedDamageError(f"Object has no attribute 'damage'.")
        damage = self.obj.get_property('damage')
        if damage is None:
            raise exceptions.UndefinedDamageError(f"Object has no attribute 'damage'.")
        return damage

    def get_range(self) -> int:
        if not self.obj.check_property('range'):
            raise exceptions.UndefinedRangeError(f"Object has no attribute 'range'.")
        weapon_range = self.obj.get_property('range')
        if weapon_range is None:
            raise exceptions.UndefinedRangeError(f"Object has no attribute 'range'.")
        return weapon_range

    def can_shoot(self) -> bool:
        if not self.obj.check_property('can_shoot'):
            raise exceptions.UndefinedRangeError(f"Object has no attribute 'can_shoot'.")
        can_shoot = self.obj.get_property('can_shoot')
        if can_shoot is None:
            raise exceptions.UndefinedRangeError(f"Object has no attribute 'can_shoot'.")
        return can_shoot
