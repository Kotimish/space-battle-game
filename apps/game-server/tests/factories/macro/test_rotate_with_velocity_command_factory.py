from src.application.commands.macro.rotate_with_velocity import RotateWithVelocityCommand
from src.domain.models.angle import Angle
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.factories.commands.macro import RotateWithVelocityCommandFactory


def test_rotate_with_velocity_factory_creates_macro_command():
    """Тест создания фабрикой RotateWithVelocityCommand с адаптерами на основе UObject"""
    uobject = DictUObject({
        "position": Vector(0, 0),
        "velocity": Vector(10, 0),
        "angle": Angle(0, 8),
        "angular_velocity": Angle(2, 8)
    })
    factory = RotateWithVelocityCommandFactory()
    command = factory.create(uobject, {})
    assert isinstance(command, RotateWithVelocityCommand)
