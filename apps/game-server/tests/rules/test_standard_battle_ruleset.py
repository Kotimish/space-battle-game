from src.domain.interfaces.ruleset import IRuleset
from src.domain.models.uobject import DictUObject
from src.infrastructure.factories.commands import ShootObjectCommandFactory
from src.infrastructure.factories.commands.macro import MoveWithFuelObjectCommandFactory
from src.infrastructure.factories.commands.macro import RotateWithVelocityCommandFactory
from src.infrastructure.rules.standard_battle_ruleset import StandardBattleRuleset


def test_interface_implementation():
    """
    Тест проверяет, что StandardBattleRuleset реализует интерфейс IRuleset.
    """
    ruleset = StandardBattleRuleset()
    assert isinstance(ruleset, IRuleset)


def test_get_initial_objects_structure():
    """
    Тест проверяет структуру и содержимое начальных объектов.
    """
    ruleset = StandardBattleRuleset()
    initial_objects = ruleset.get_initial_objects()

    # Проверяем, что возвращается словарь
    assert isinstance(initial_objects, dict)

    # Проверяем количество объектов
    assert len(initial_objects) == 6

    # Проверяем наличие ключей и типов объектов
    expected_keys = [f"fleet_red_{i}" for i in range(3)] + [f"fleet_blue_{i}" for i in range(3)]
    for key in expected_keys:
        assert key in initial_objects
        assert isinstance(initial_objects[key], DictUObject)


def test_initial_object_properties(initial_object_standard_battle_ruleset):
    """
    Тест проверяет конкретные свойства каждого из начальных объектов.
    """
    ruleset = StandardBattleRuleset()
    initial_objects = ruleset.get_initial_objects()

    for ship_key, expected_values in initial_object_standard_battle_ruleset.items():
        ship = initial_objects[ship_key]

        assert ship.get_property("position") == expected_values["position"]
        assert ship.get_property("velocity") == expected_values["velocity"]
        assert ship.get_property("health_points") == expected_values["health_points"]
        assert ship.get_property("damage") == expected_values["damage"]
        assert ship.get_property("range") == expected_values["range"]
        assert ship.get_property("fuel_level") == expected_values["fuel_level"]
        assert ship.get_property("fuel_consumption") == expected_values["fuel_consumption"]


def test_get_allowed_operations_structure():
    """
    Тест проверяет структуру и содержимое разрешённых операций.
    """
    ruleset = StandardBattleRuleset()
    allowed_operations = ruleset.get_allowed_operations()

    # Проверяем, что возвращается словарь
    assert isinstance(allowed_operations, dict), "Возвращаемое значение должно быть словарём."

    # Проверяем наличие ожидаемых операций
    expected_operations = ["movement", "rotation", "shoot"]
    for op_id in expected_operations:
        assert op_id in allowed_operations, f"Операция '{op_id}' должна быть в разрешённых."

    # Проверяем, что значения - это классы фабрик команд
    assert allowed_operations["movement"] == MoveWithFuelObjectCommandFactory
    assert allowed_operations["rotation"] == RotateWithVelocityCommandFactory
    assert allowed_operations["shoot"] == ShootObjectCommandFactory
