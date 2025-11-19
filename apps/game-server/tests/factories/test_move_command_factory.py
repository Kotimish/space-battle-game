from src.application.commands.move import MoveCommand
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.factories.commands.create_move_command import MoveObjectCommandFactory


def test_move_object_command_factory_creates_move_command():
    """Тест создания фабрикой MoveCommand с адаптером на основе UObject"""
    uobject = DictUObject({
        "position": Vector(0, 0),
        "velocity": Vector(1, 0)
    })

    factory = MoveObjectCommandFactory()
    command = factory.create(uobject, {})

    assert isinstance(command, MoveCommand)


def test_move_object_command_factory_sets_velocity_from_arguments():
    """Тест установки фабрикой velocity из arguments при наличии"""
    uobject = DictUObject({
        "position": Vector(0, 0)
    })

    factory = MoveObjectCommandFactory()
    command = factory.create(uobject, {"velocity": {"x": 5, "y": -3}})

    assert uobject.get_property("velocity") == Vector(5, -3)
    assert isinstance(command, MoveCommand)
