from abc import ABC

from src.domain.interfaces.fuel_consumer_object import IFuelConsumerObject
from src.domain.interfaces.movable_object import IMovableObject


class IMoveFuelConsumer(IMovableObject, IFuelConsumerObject, ABC):
    """Интефейс для движущихся объектов, которые потребляют топливо"""
