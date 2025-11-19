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
