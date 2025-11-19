from src.domain.interfaces.damageable_object import IDamageableObject
from src.domain.interfaces.uobject import UObject
from src.domain.exceptions import shoot as exceptions


class DamageableObjectAdapter(IDamageableObject):
    """
    Адаптер, позволяющий UObject реализовать интерфейс IDamageableObject.
    Предполагает, что UObject имеет свойства 'health_points'.
    """

    def __init__(self, obj: UObject):
        self.obj = obj

    def get_health_points(self) -> int:
        if not self.obj.check_property('health_points'):
            raise exceptions.UndefinedHealthPointError(f"Object has no attribute 'health_points'.")
        health_points = self.obj.get_property('health_points')
        if health_points is None:
            raise exceptions.UndefinedHealthPointError(f"Object has no attribute 'health_points'.")
        return health_points

    def set_health_points(self, health_points: int) -> None:
        max_health_points = max(0, health_points)
        self.obj.set_property('health_points', max_health_points)

    def is_alive(self) -> bool:
        return self.get_health_points() > 0
