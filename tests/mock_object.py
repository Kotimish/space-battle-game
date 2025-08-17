from typing import Any

from src.interfaces.uobject import UObject


class MockUObject(UObject):
    def __init__(self, data: dict = None):
        self.property_dict: dict[str, Any] = data or {}

    def get_property(self, key: str) -> Any:
        return self.property_dict.get(key)

    def set_property(self, key: str, value: Any) -> None:
        self.property_dict[key] = value

    def check_property(self, key: str) -> bool:
        return key in self.property_dict

    def __str__(self) -> str:
        return f'Mock object: {self.property_dict}'
