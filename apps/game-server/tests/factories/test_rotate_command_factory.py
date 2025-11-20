from src.application.commands.rotate import RotateCommand
from src.domain.models.angle import Angle
from src.domain.models.uobject import DictUObject
from src.infrastructure.factories.commands import RotateCommandFactory


def test_rotate_command_factory_creates_rotate_command():
    """Тест создания фабрикой RotateCommand с адаптером на основе UObject"""
    uobject = DictUObject({
        "angle": Angle(0, 8),
        "angular_velocity": Angle(2, 8)
    })
    factory = RotateCommandFactory()
    command = factory.create(uobject, {})
    assert isinstance(command, RotateCommand)


def test_rotate_command_factory_sets_angular_velocity_from_arguments():
    """Тест установки angular_velocity через arguments"""
    uobject = DictUObject({
        "angle": Angle(1, 8)
    })
    factory = RotateCommandFactory()
    command = factory.create(uobject, {
        "angular_velocity": {"direction": 3, "directions_number": 8}
    })
    assert uobject.get_property("angular_velocity") == Angle(3, 8)
    assert isinstance(command, RotateCommand)
