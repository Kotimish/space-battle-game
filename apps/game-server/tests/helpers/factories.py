from src.domain.models.angle import Angle
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.adapters.damageable_object_adapter import DamageableObjectAdapter
from src.infrastructure.adapters.fuel_consumer_adapter import FuelConsumerAdapter
from src.infrastructure.adapters.movable_adapter import MovableObjectAdapter
from src.infrastructure.adapters.movable_with_velocity_adapter import MovableWithVelocityAdapter
from src.infrastructure.adapters.move_fuel_consumer_adapter import MoveFuelConsumer
from src.infrastructure.adapters.rotatable_adapter import RotatableObjectAdapter
from src.infrastructure.adapters.shootable_object_adapter import ShootableObjectAdapter
from src.infrastructure.adapters.targetable_object_adapter import TargetableObjectAdapter
from src.infrastructure.adapters.weapon_object_adapter import WeaponObjectAdapter


def make_rotatable_object(angle: Angle, angular_velocity: Angle) -> RotatableObjectAdapter:
    data = {"angle": angle, "angular_velocity": angular_velocity}
    uobject = DictUObject(data)
    rotatable_object = RotatableObjectAdapter(uobject)
    return rotatable_object


def make_movable_object(position: Vector, velocity: Vector) -> MovableObjectAdapter:
    data = {"position": position, "velocity": velocity}
    uobject = DictUObject(data)
    movable_object = MovableObjectAdapter(uobject)
    return movable_object


def make_fuel_consumer_object(fuel_level: int, fuel_consumption: int) -> FuelConsumerAdapter:
    data = {"fuel_level": fuel_level, "fuel_consumption": fuel_consumption}
    uobject = DictUObject(data)
    fuel_consumer_object = FuelConsumerAdapter(uobject)
    return fuel_consumer_object


def make_movable_with_velocity_object(position: Vector, velocity: Vector) -> MovableWithVelocityAdapter:
    data = {"position": position, "velocity": velocity}
    uobject = DictUObject(data)
    movable_object = MovableWithVelocityAdapter(uobject)
    return movable_object


def make_movable_fuel_consumer(
        position: Vector,
        velocity: Vector,
        fuel_level: int,
        fuel_consumption: int
) -> MoveFuelConsumer:
    data = {
        "position": position,
        "velocity": velocity,
        "fuel_level": fuel_level,
        "fuel_consumption": fuel_consumption
    }
    uobject = DictUObject(data)
    movable_object = MoveFuelConsumer(uobject)
    return movable_object


def make_weapon_object(
        weapon_damage: int,
        weapon_range: int,
        can_shoot: bool
) -> WeaponObjectAdapter:
    data = {
        "damage": weapon_damage,
        "range": weapon_range,
        "can_shoot": can_shoot,
    }
    uobject = DictUObject(data)
    weapon_object = WeaponObjectAdapter(uobject)
    return weapon_object


def make_shooter_object(
        position: Vector,
        velocity: Vector,
        weapon_damage: int,
        weapon_range: int,
        can_shoot: bool
) -> ShootableObjectAdapter:
    data = {
        "position": position,
        "velocity": velocity,
        "damage": weapon_damage,
        "range": weapon_range,
        "can_shoot": can_shoot,
    }
    uobject = DictUObject(data)
    shooter_object = ShootableObjectAdapter(uobject)
    return shooter_object


def make_damageable_object(
        health_points: int
) -> DamageableObjectAdapter:
    data = {
        "health_points": health_points,
    }
    uobject = DictUObject(data)
    damageable_object = DamageableObjectAdapter(uobject)
    return damageable_object


def make_targetable_object(
        position: Vector,
        velocity: Vector,
        health_points: int
) -> TargetableObjectAdapter:
    data = {
        "position": position,
        "velocity": velocity,
        "health_points": health_points,
    }
    uobject = DictUObject(data)
    targetable_object = TargetableObjectAdapter(uobject)
    return targetable_object
