from typing import Callable, Any

from src.factories.commands.create_move_with_fuel_command import MoveWithFuelObjectCommandFactory
from src.factories.operation_router import OperationToCommandRouter
from src.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.interfaces.ruleset import IRuleset
from src.interfaces.uobject import UObject
from src.models.game_session import GameSession
from src.models.uobject import DictUObject
from src.models.vector import Vector


class TestRuleset(IRuleset):
    """Шаблон операций для тестирования"""

    def get_initial_objects(self) -> dict[str, UObject]:
        return {
            "object_0": DictUObject({
                "position": Vector(0, 0),
                "velocity": Vector(10, 0),
                "fuel_level": 100,
                "fuel_consumption": 10,
            })
        }

    def get_allowed_operations(self) -> dict[str, type[IObjectCommandFactory]]:
        return {
            # Команда движения для простых тестов
            "movement": MoveWithFuelObjectCommandFactory,
        }

    def get_dependencies(self, game_id: str, session: GameSession) -> dict[str, Callable[..., Any]]:
        router = OperationToCommandRouter(self.get_allowed_operations())
        dependencies = {
            'Game.Object.GetAll': lambda: session.get_all_objects(),
            'Game.Object.Get': lambda obj_id: session.get_object_by_id(obj_id),
            # Регистрируем OperationToCommandMap
            'OperationToCommandMap': lambda operation_id: router.get_factory(operation_id)
        }
        return dependencies
