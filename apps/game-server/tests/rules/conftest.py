import pytest

from src.domain.models.vector import Vector


@pytest.fixture
def initial_object_standard_battle_ruleset() -> dict[str, dict]:
    return {
        "fleet_red_0": {
            "position": Vector(-200, -100),
            "velocity": Vector(0, 0),
            "health_points": 100,
            "damage": 20,
            "range": 300,
            "fuel_level": 1000,
            "fuel_consumption": 1
        },
        "fleet_red_1": {
            "position": Vector(-200, 0),
            "velocity": Vector(0, 0),
            "health_points": 100,
            "damage": 20,
            "range": 300,
            "fuel_level": 1000,
            "fuel_consumption": 1
        },
        "fleet_red_2": {
            "position": Vector(-200, 100),
            "velocity": Vector(0, 0),
            "health_points": 100,
            "damage": 20,
            "range": 300,
            "fuel_level": 1000,
            "fuel_consumption": 1
        },
        "fleet_blue_0": {
            "position": Vector(200, -100),
            "velocity": Vector(0, 0),
            "health_points": 100,
            "damage": 20,
            "range": 300,
            "fuel_level": 1000,
            "fuel_consumption": 1
        },
        "fleet_blue_1": {
            "position": Vector(200, 0),
            "velocity": Vector(0, 0),
            "health_points": 100,
            "damage": 20,
            "range": 300,
            "fuel_level": 1000,
            "fuel_consumption": 1
        },
        "fleet_blue_2": {
            "position": Vector(200, 100),
            "velocity": Vector(0, 0),
            "health_points": 100,
            "damage": 20,
            "range": 300,
            "fuel_level": 1000,
            "fuel_consumption": 1
        },
    }
