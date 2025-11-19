from typing import Any

from src.application.commands.shoot import ShootCommand
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.infrastructure.adapters.shootable_object_adapter import ShootableObjectAdapter
from src.infrastructure.adapters.targetable_object_adapter import TargetableObjectAdapter
from src.infrastructure.dependencies.ioc import IoC


class ShootObjectCommandFactory(IObjectCommandFactory):
    """
    Фабрика для команды выстрела.
    Предполагает, что UObject содержит все необходимые свойства:
    - position, velocity — для получения информации об позиции объекта.
    - damage, range, can_shoot — для получения информации об оружие объекта.
    """
    def create(self, game_object: UObject, arguments: dict[str, Any]) -> BaseCommand:
        shooter = ShootableObjectAdapter(game_object)
        # Получаем все цели из сессии (кроме самого стреляющего)
        all_objects = IoC[dict[str, UObject]].resolve('Game.Session.GetAll')
        targets = [TargetableObjectAdapter(obj) for idx, obj in all_objects.items()]
        return ShootCommand(shooter=shooter, targets=targets)
