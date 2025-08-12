from src.exceptions.move import UndefinedPositionError, UndefinedVelocityError
from src.interfaces.movable_object import IMovableObject
from src.interfaces.uobject import UObject
from src.models.vector import Vector


class MovableObjectAdapter(IMovableObject):
    def __init__(self, obj: UObject):
        self.obj = obj

    def get_position(self) -> Vector:
        if not self.obj.check_property('position'):
            raise UndefinedPositionError(f"Object has no attribute 'position'.")
        position = self.obj.get_property('position')
        if position is None:
            raise UndefinedPositionError(f"Object has no attribute 'position'.")
        return position

    def get_velocity(self) -> Vector:
        if not self.obj.check_property('velocity'):
            raise UndefinedVelocityError(f"Object has no attribute 'velocity'.")
        velocity = self.obj.get_property('velocity')
        if velocity is None:
            raise UndefinedVelocityError(f"Object has no attribute 'velocity'.")
        return velocity

    def set_position(self, position: Vector) -> None:
        self.obj.set_property('position', position)
