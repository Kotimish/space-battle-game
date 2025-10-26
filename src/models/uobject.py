from typing import Any
from src.interfaces.uobject import UObject

# Стандартные типы данных
STANDARD_TYPES = (int, float, str, bool,)

class DictUObject(UObject):
    def __init__(self, data: dict = None):
        self.property_dict: dict[str, Any] = data or {}

    def get_property(self, key: str) -> Any:
        return self.property_dict.get(key)

    def set_property(self, key: str, value: Any) -> None:
        self.property_dict[key] = value

    def check_property(self, key: str) -> bool:
        return key in self.property_dict

    def to_dict(self) -> dict[str, Any]:
        result = {}
        for key, value in self.property_dict.items():
            if isinstance(value, STANDARD_TYPES):
                result[key] = value
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()
        return result


    def __str__(self) -> str:
        return f'Object: {self.property_dict}'
