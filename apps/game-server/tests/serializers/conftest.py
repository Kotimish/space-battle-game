import pytest

from src.application.services.serializers.dict_uobject_serializer import DictUObjectSerializer
from src.application.services.serializers.type_registry import TypeRegistry
from src.domain.models.angle import Angle
from src.domain.models.vector import Vector


@pytest.fixture
def serializer() -> DictUObjectSerializer:
    registry = TypeRegistry()
    registry.register("Vector", Vector)
    registry.register("Angle", Angle)
    return DictUObjectSerializer(registry.get_registry())
