from typing import Any

from src.interfaces.serializers.serializable import Serializable
from src.interfaces.uobject import UObject
from src.interfaces.serializers.uobject_serializer import IGameObjectSerializer
from src.models.uobject import DictUObject

# Стандартные типы, которые не требуют специальной сериализации
STANDARD_TYPES = (int, float, str, bool, type(None))


class DictUObjectSerializer(IGameObjectSerializer):
    """
    Сериализатор для DictUObject с поддержкой вложенных ISerializable-объектов.
    Использует реестр типов для безопасной десериализации.
    """
    def __init__(self, type_registry: dict[str, type[Serializable]]):
        self._type_registry = type_registry

    def serialize(self, obj: UObject) -> dict:
        """Рекурсивная сериализация с поддержкой Serializable"""
        if not isinstance(obj, DictUObject):
            raise TypeError(f"Unsupported UObject type: {type(obj)}")
        return self._serialize_dict(obj.property_dict)

    def deserialize(self, data: dict) -> UObject:
        """Рекурсивная десериализация с восстановлением типов"""
        restored = self._deserialize_dict(data)
        return DictUObject(restored)

    def _serialize_dict(self, value_dict: dict) -> dict:
        return {
            key: self._serialize_value(value)
            for key, value in value_dict.items()
        }

    def _serialize_value(self, value: Any) -> Any:
        if isinstance(value, Serializable):
            type_name = self._get_type_name(value)
            return {
                "__type__": type_name,
                "__data__": value.serialize()
            }
        elif isinstance(value, STANDARD_TYPES):
            return value
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return self._serialize_dict(value)
        else:
            raise TypeError(f"Cannot serialize value of type {type(value)}")

    def _deserialize_dict(self, value_dict: dict) -> dict:
        return {
            key: self._deserialize_value(value)
            for key, value in value_dict.items()
        }

    def _deserialize_value(self, value: Any) -> Any:
        if isinstance(value, dict):
            if "__type__" in value and "__data__" in value:
                type_name = value["__type__"]
                data = value["__data__"]
                cls = self._get_class_by_name(type_name)
                return cls.serialize(data)
            else:
                return self._deserialize_dict(value)
        elif isinstance(value, list):
            return [self._deserialize_value(item) for item in value]
        else:
            return value

    def _get_type_name(self, obj: Serializable) -> str:
        for name, cls in self._type_registry.items():
            if isinstance(obj, cls):
                return name
        raise ValueError(f"Unregistered serializable type: {type(obj)}")

    def _get_class_by_name(self, name: str) -> type[Serializable]:
        if name not in self._type_registry:
            raise ValueError(f"Unknown serializable type name: {name}")
        return self._type_registry[name]