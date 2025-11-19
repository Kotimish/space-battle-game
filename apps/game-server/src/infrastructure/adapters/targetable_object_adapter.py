from src.domain.interfaces.targetable_object import ITargetableObject
from src.domain.interfaces.uobject import UObject
from src.infrastructure.adapters.damageable_object_adapter import DamageableObjectAdapter
from src.infrastructure.adapters.movable_adapter import MovableObjectAdapter


class TargetableObjectAdapter(MovableObjectAdapter, DamageableObjectAdapter, ITargetableObject):
    """
    Адаптер, объединяющий IMovableObject и IDamageableObject.
    """

    def __init__(self, obj: UObject):
        super().__init__(obj)
