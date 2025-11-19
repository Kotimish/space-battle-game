from src.application.services.serializers.dict_uobject_serializer import DictUObjectSerializer
from src.application.services.serializers.type_registry import TypeRegistry
from src.domain.interfaces.serializers.uobject_serializer import IGameObjectSerializer
from src.domain.models.angle import Angle
from src.domain.models.vector import Vector


def setup_serializer() -> IGameObjectSerializer:
    # Регистрация сериализуемых типов
    type_registry = TypeRegistry()
    type_registry.register("Vector", Vector)
    type_registry.register("Angle", Angle)
    serializer = DictUObjectSerializer(type_registry.get_registry())
    return serializer
