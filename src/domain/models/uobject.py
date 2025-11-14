from typing import Any

from src.domain.interfaces.serializers.serializable import Serializable
from src.domain.interfaces.uobject import UObject

# Стандартные типы данных
STANDARD_TYPES = (int, float, str, bool, type(None))

class DictUObject(UObject):
    def __init__(self, data: dict = None):
        self.property_dict: dict[str, Any] = data or {}

    def get_property(self, key: str) -> Any:
        return self.property_dict.get(key)

    def set_property(self, key: str, value: Any) -> None:
        self.property_dict[key] = value

    def check_property(self, key: str) -> bool:
        return key in self.property_dict

    def _to_dict(self, value) -> Any:
        if isinstance(value, Serializable):
            return value.to_dict()
        elif isinstance(value, STANDARD_TYPES):
            return value
        elif isinstance(value, (list, tuple)):
            return [
                self._to_dict(item)
                for item in value
            ]
        elif isinstance(value, dict):
            return {
                str(dict_key): self._to_dict(dict_value)
                for dict_key, dict_value in value.items()
            }
        else:
            raise TypeError(f"Cannot serialize value of type {type(value)}: {value}")

    def to_dict(self) -> dict[str, Any]:
        return {
            key: self._to_dict(value)
            for (key), value in self.property_dict.items()
        }


    def __str__(self) -> str:
        return f'Object: {self.property_dict}'
