import pytest

from src.domain.models.angle import Angle
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector


def test_serialize_standard_types(serializer):
    """Тест сериализации стандартных типов"""
    uobject = DictUObject({
        "int_value": 42,
        "str_value": "any_text",
        "bool_value": True,
        "none_value": None,
    })
    result = serializer.serialize(uobject)
    expected = {
        "int_value": 42,
        "str_value": "any_text",
        "bool_value": True,
        "none_value": None,
    }
    assert result == expected


def test_serialize_serializable(serializer):
    """Тест сериализации моделей типа объект-значение"""
    uobject = DictUObject({
        "vector": Vector(10, 0),
        "angle": Angle(3, 8)
    })
    result = serializer.serialize(uobject)
    expected = {
        "vector": {
            "__type__": "Vector",
            "__data__": {"x": 10, "y": 0}
        },
        "angle": {
            "__type__": "Angle",
            "__data__": {"direction": 3, "directions_number": 8}
        }
    }
    assert result == expected


def test_serialize_nested_list_and_dict(serializer):
    """Тест рекурсивной сериализации списков и словарей"""
    uobject = DictUObject({
        "items": [
            Vector(10, 0),
            Vector(0, 10)
        ],
        "meta": {
            "main": Vector(10, 10),
            "tags": ["a", "b"]
        }
    })
    result = serializer.serialize(uobject)
    expected = {
        "items": [
            {"__type__": "Vector", "__data__": {"x": 10, "y": 0}},
            {"__type__": "Vector", "__data__": {"x": 0, "y": 10}},
        ],
        "meta": {
            "main": {"__type__": "Vector", "__data__": {"x": 10, "y": 10}},
            "tags": ["a", "b"]
        }
    }
    assert result == expected


def test_serialize_unsupported_type(serializer):
    """Тест неподдерживаемых сериализацией типов данных"""

    class CustomClass:
        """Класс-пустышка"""

    uobject = DictUObject({"custom": CustomClass()})
    with pytest.raises(TypeError):
        serializer.serialize(uobject)


def test_deserialize_standard_types(serializer):
    """Тест десериализации стандартных типов"""
    data = {
        "int_value": 42,
        "str_value": "any_test",
        "bool_value": False,
        "none_value": None
    }
    uobject = serializer.deserialize(data)
    assert uobject.get_property("int_value") == 42
    assert uobject.get_property("str_value") == "any_test"
    assert uobject.get_property("bool_value") is False
    assert uobject.get_property("none_value") is None


def test_deserialize_serializable(serializer):
    """Тест десериализации моделей типа объект-значение"""
    data = {
        "vector": {
            "__type__": "Vector",
            "__data__": {"x": 10, "y": 0}
        },
        "angle": {
            "__type__": "Angle",
            "__data__": {"direction": 3, "directions_number": 8}
        }
    }
    uobject = serializer.deserialize(data)
    vector = uobject.get_property("vector")
    angle = uobject.get_property("angle")
    assert isinstance(vector, Vector)
    assert vector == Vector(10, 0)
    assert isinstance(angle, Angle)
    assert angle == Angle(3, 8)


def test_deserialize_nested_structures(serializer):
    """Тест рекурсивной десериализации списков и словарей"""
    data = {
        "items": [
            {"__type__": "Vector", "__data__": {"x": 10, "y": 0}},
            {"__type__": "Vector", "__data__": {"x": 0, "y": 10}}
        ],
        "meta": {
            "main": {"__type__": "Vector", "__data__": {"x": 10, "y": 10}},
            "tags": ["a", "b"]
        }
    }
    uobject = serializer.deserialize(data)
    items = uobject.get_property("items")
    config = uobject.get_property("meta")
    assert isinstance(items, list)
    assert len(items) == 2
    assert items[0] == Vector(10, 0)
    assert items[1] == Vector(0, 10)
    assert config["main"] == Vector(10, 10)
    assert config["tags"] == ["a", "b"]


def test_deserialize_unsupported_type(serializer):
    """Тест неподдерживаемых десериализацией типов данных"""
    data = {
        "obj": {
            "__type__": "UnknownType",
            "__data__": {}
        }
    }
    with pytest.raises(ValueError):
        serializer.deserialize(data)


def test_deserialize_missing_type_or_data_keys(serializer):
    """Тест десериализации моделей типа объект-значение без __type__"""
    data = {
        "bad_vector": {
            # отсутствует __type__
            "__data__": {"x": 10, "y": 0}
        }
    }
    uobject = serializer.deserialize(data)
    # Стандартный тип данных вместо модели объект-значения
    assert uobject.get_property("bad_vector") == data['bad_vector']


def test_deserialize_invalid_serializable_missing_keys(serializer):
    """Тест десериализации моделей типа объект-значение без __data__"""
    # Если есть __type__, но нет __data__ → ошибка при вызове .serialize()
    data = {
        "bad_vector": {
            "__type__": "Vector"
            # отсутствует __data__
        }

    }
    uobject = serializer.deserialize(data)
    # Стандартный тип данных вместо модели объект-значения
    assert uobject.get_property("bad_vector") == data['bad_vector']
