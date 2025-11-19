import pytest
from src.application.commands.shoot import ShootCommand
from src.domain.interfaces.damageable_object import IDamageableObject
from src.domain.interfaces.shootable_object import IShootableObject
from src.domain.interfaces.targetable_object import ITargetableObject
from src.domain.interfaces.weapon_object import IWeaponObject
from src.infrastructure.adapters.damageable_object_adapter import DamageableObjectAdapter
from src.infrastructure.adapters.shootable_object_adapter import ShootableObjectAdapter
from src.infrastructure.adapters.targetable_object_adapter import TargetableObjectAdapter
from src.infrastructure.adapters.weapon_object_adapter import WeaponObjectAdapter
from src.domain.interfaces.uobject import UObject
from src.domain.models.vector import Vector
from tests.helpers.factories import make_shooter_object, make_targetable_object

from src.domain.exceptions import shoot as exceptions


def test_shoot_command_executes_successfully():
    """Тест успешного выполнения команды стрельбы."""
    # Создание адаптеров
    shooter_object: ShootableObjectAdapter = make_shooter_object(
        weapon_damage=20,
        weapon_range=10,
        can_shoot=True,
        position=Vector(5,5),
        velocity=Vector(0, 0)
    )
    target_object: TargetableObjectAdapter = make_targetable_object(
        health_points=100,
        position=Vector(5,5),
        velocity=Vector(0, 0)
    )

    # Проверка начального состояния
    assert target_object.get_health_points() == 100
    # Выполняем команду стрельбы
    command = ShootCommand(shooter_object, [target_object])
    command.execute()

    # Проверяем, что здоровье цели уменьшилось
    assert target_object.get_health_points() < 100
    # Предполагаем, что урон наносится из свойства damage объекта
    assert target_object.get_health_points() == 80


def test_shoot_command_with_unavailable_weapon():
    """Тест команды стрельбы с недоступным для стрельбы оружием."""
    # Создание адаптеров
    shooter_object: ShootableObjectAdapter = make_shooter_object(
        weapon_damage=20,
        weapon_range=10,
        can_shoot=False,
        position=Vector(5,5),
        velocity=Vector(0, 0)
    )
    target_object: TargetableObjectAdapter = make_targetable_object(
        health_points=100,
        position=Vector(5,5),
        velocity=Vector(0, 0)
    )

    # Выполняем команду стрельбы
    command = ShootCommand(shooter_object, [target_object])
    with pytest.raises(exceptions.WeaponCanNotShootError):
        command.execute()


def test_shoot_command_with_unavailable_enemy():
    """Тест команды стрельбы по врагу вне радиуса поражения."""
    # Создание адаптеров
    shooter_object: ShootableObjectAdapter = make_shooter_object(
        weapon_damage=20,
        weapon_range=10,
        can_shoot=True,
        position=Vector(50,50),
        velocity=Vector(0, 0)
    )
    target_object: TargetableObjectAdapter = make_targetable_object(
        health_points=100,
        position=Vector(5,5),
        velocity=Vector(0, 0)
    )

    # Проверка начального состояния
    assert target_object.get_health_points() == 100
    # Выполняем команду стрельбы
    command = ShootCommand(shooter_object, [target_object])
    command.execute()

    # Проверяем, что здоровье цели не изменилось
    assert target_object.get_health_points() == 100