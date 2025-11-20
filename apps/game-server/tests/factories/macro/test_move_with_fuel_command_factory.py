from src.application.commands.macro.move_with_fuel_command import MoveWithFuelCommand
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.factories.commands.macro.create_move_with_fuel_command import MoveWithFuelObjectCommandFactory


def test_move_with_fuel_factory_creates_macro_command():
    """Тест создания фабрикой MoveWithFuelCommand с адаптером на основе UObject"""
    uobject = DictUObject({
        "position": Vector(0, 0),
        "velocity": Vector(10, 0),
        "fuel_level": 100,
        "fuel_consumption": 5
    })

    factory = MoveWithFuelObjectCommandFactory()
    command = factory.create(uobject, {})

    assert isinstance(command, MoveWithFuelCommand)


def test_move_with_fuel_factory_sets_velocity_from_arguments():
    """Тест установки фабрикой velocity из arguments при наличии"""
    uobject = DictUObject({
        "position": Vector(0, 0),
        "fuel_level": 100,
        "fuel_consumption": 10
    })

    factory = MoveWithFuelObjectCommandFactory()
    command = factory.create(uobject, {"velocity": {"x": 20, "y": 0}})

    assert uobject.get_property("velocity") == Vector(20, 0)
    assert isinstance(command, MoveWithFuelCommand)
