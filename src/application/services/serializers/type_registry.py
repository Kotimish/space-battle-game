from typing import Dict, Type
from src.domain.interfaces.serializers.serializable import Serializable

class TypeRegistry:
    def __init__(self):
        self._registry: Dict[str, Type[Serializable]] = {}

    def register(self, name: str, cls: Type[Serializable]) -> None:
        if not hasattr(cls, 'serialize') or not hasattr(cls, 'deserialize'):
            raise TypeError(f"Class {cls} must implement serialize() and deserialize()")
        self._registry[name] = cls

    def get_registry(self) -> Dict[str, Type[Serializable]]:
        return self._registry.copy()