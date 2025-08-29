from abc import ABC, abstractmethod

from src.interfaces.fuel_consumer_object import IFuelConsumerObject
from src.interfaces.movable_object import IMovableObject


class IMoveFuelConsumer(IMovableObject, IFuelConsumerObject, ABC):
    """Интефейс для движущихся объектов, которые потребляют топливо"""
