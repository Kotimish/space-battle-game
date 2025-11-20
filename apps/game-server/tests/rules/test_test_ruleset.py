from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.rules.test_ruleset import TestRuleset


def test_get_initial_objects():
    """
    Тест проверяет, что TestRuleset возвращает ожидаемый начальный объект.
    """
    ruleset = TestRuleset()
    initial_objects = ruleset.get_initial_objects()

    # Проверяем, что возвращается словарь
    assert isinstance(initial_objects, dict)
    # Проверяем количество объектов
    assert len(initial_objects) == 1
    assert "object_0" in initial_objects

    obj = initial_objects["object_0"]
    assert isinstance(obj, DictUObject)

    # Проверяем конкретные значения свойств объекта
    expected_data = {
        "position": Vector(0, 0),
        "velocity": Vector(10, 0),
        "fuel_level": 100,
        "fuel_consumption": 10,
    }

    for key, expected_value in expected_data.items():
        assert obj.get_property(key) == expected_value


def test_get_allowed_operations():
    """
    Тест проверяет, что TestRuleset возвращает пустой словарь
    для разрешённых операций (в текущей реализации).
    """
    expected_operations = ["movement",]

    ruleset = TestRuleset()
    allowed_operations = ruleset.get_allowed_operations()

    assert isinstance(allowed_operations, dict)
    for operation_id in expected_operations:
        assert operation_id in allowed_operations


def test_interface_implementation():
    """
    Тест проверяет, что TestRuleset реализует интерфейс IRuleset.
    """
    from src.domain.interfaces.ruleset import IRuleset
    ruleset = TestRuleset()
    # TestRuleset должен реализовывать интерфейс IRuleset
    assert isinstance(ruleset, IRuleset)
