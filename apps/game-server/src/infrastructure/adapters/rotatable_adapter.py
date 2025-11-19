from src.domain.exceptions.rotate import UndefinedAngleError, UndefinedAngularVelocityError
from src.domain.interfaces.rotatable_object import IRotatableObject
from src.domain.interfaces.uobject import UObject
from src.domain.models.angle import Angle


class RotatableObjectAdapter(IRotatableObject):
    def __init__(self, obj: UObject):
        self.obj = obj

    def get_angle(self) -> Angle:
        if not self.obj.check_property('angle'):
            raise UndefinedAngleError(f"Object has no attribute 'angle'.")
        angle = self.obj.get_property('angle')
        if angle is None:
            raise UndefinedAngleError(f"Object has no attribute 'angle'.")
        return angle

    def get_angular_velocity(self) -> Angle:
        if not self.obj.check_property('angular_velocity'):
            raise UndefinedAngularVelocityError(f"Object has no attribute 'angular_velocity'.")
        angular_velocity = self.obj.get_property('angular_velocity')
        if angular_velocity is None:
            raise UndefinedAngularVelocityError(f"Object has no attribute 'angular_velocity'.")
        return angular_velocity

    def set_angle(self, angle: Angle) -> None:
        self.obj.set_property('angle', angle)
