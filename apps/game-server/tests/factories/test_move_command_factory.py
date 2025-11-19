from src.application.commands.move import MoveCommand
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.factories.commands import MoveObjectCommandFactory


def test_move_object_command_factory_creates_move_command():
    """Тест создания фабрикой MoveCommand с адаптером на основе UObject"""
    uobject = DictUObject({
        "position": Vector(0, 0),
        "velocity": Vector(1, 0)
    })

    factory = MoveObjectCommandFactory()
    command = factory.create(uobject, {})

    assert isinstance(command, MoveCommand)
