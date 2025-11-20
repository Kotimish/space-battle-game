from src.application.commands.shoot import ShootCommand
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.factories.commands.create_shoot_command import ShootObjectCommandFactory


def test_shoot_command_factory_creates_shoot_command():
    """Тест создания фабрикой ShootCommand с адаптерами"""
    shooter = DictUObject({
        "position": Vector(0, 0),
        "velocity": Vector(1, 0),
        "damage": 20,
        "range": 300,
        "can_shoot": True
    })

    factory = ShootObjectCommandFactory()
    command = factory.create(shooter, {})

    assert isinstance(command, ShootCommand)
