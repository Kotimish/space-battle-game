from src.adapters.fuel_consumer_adapter import FuelConsumerAdapter
from src.adapters.movable_adapter import MovableObjectAdapter
from src.adapters.movable_with_velocity_adapter import MovableWithVelocityAdapter
from src.adapters.move_fuel_consumer_adapter import MoveFuelConsumer
from src.adapters.rotatable_adapter import RotatableObjectAdapter
from src.models.angle import Angle
from src.models.vector import Vector
from tests.mock_object import MockUObject


def make_rotatable_object(angle: Angle, angular_velocity: Angle) -> RotatableObjectAdapter:
    data = {"angle": angle, "angular_velocity": angular_velocity}
    mock_object = MockUObject(data)
    rotatable_object = RotatableObjectAdapter(mock_object)
    return rotatable_object


def make_movable_object(position: Vector, velocity: Vector) -> MovableObjectAdapter:
    data = {"position": position, "velocity": velocity}
    mock_object = MockUObject(data)
    movable_object = MovableObjectAdapter(mock_object)
    return movable_object


def make_fuel_consumer_object(fuel_level: int, fuel_consumption: int) -> FuelConsumerAdapter:
    data = {"fuel_level": fuel_level, "fuel_consumption": fuel_consumption}
    mock_object = MockUObject(data)
    fuel_consumer_object = FuelConsumerAdapter(mock_object)
    return fuel_consumer_object


def make_movable_with_velocity_object(position: Vector, velocity: Vector) -> MovableWithVelocityAdapter:
    data = {"position": position, "velocity": velocity}
    mock_object = MockUObject(data)
    movable_object = MovableWithVelocityAdapter(mock_object)
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
    mock_object = MockUObject(data)
    movable_object = MoveFuelConsumer(mock_object)
    return movable_object
