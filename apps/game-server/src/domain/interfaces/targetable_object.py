from abc import ABC

from src.domain.interfaces.damageable_object import IDamageableObject
from src.domain.interfaces.movable_object import IMovableObject


class ITargetableObject(IDamageableObject, IMovableObject, ABC):
    """Интерфейс для объекта, который может быть целью: имеет позицию и здоровье."""