from typing import Any

from src.infrastructure.adapters.movable_adapter import MovableObjectAdapter
from src.application.commands.move import MoveCommand
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.domain.models.vector import Vector


class MoveObjectCommandFactory(IObjectCommandFactory):
    """Фабрика для команды движения"""
    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        adapter = MovableObjectAdapter(game_object)
        return MoveCommand(adapter)
