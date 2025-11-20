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


def test_rotate_with_velocity_factory_sets_angular_velocity_from_arguments():
    """Тест установки angular_velocity через arguments"""
    uobject = DictUObject({
        "position": Vector(0, 0),
        "velocity": Vector(5, 0),
        "angle": Angle(1, 8)
    })
    factory = RotateWithVelocityCommandFactory()
    command = factory.create(uobject, {
        "angular_velocity": {"direction": 4, "directions_number": 8}
    })
    assert uobject.get_property("angular_velocity") == Angle(4, 8)
    assert isinstance(command, RotateWithVelocityCommand)
