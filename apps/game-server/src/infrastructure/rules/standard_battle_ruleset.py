from typing import Callable, Any, Dict

from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.ruleset import IRuleset
from src.domain.interfaces.uobject import UObject
from src.domain.models.game_session import GameSession
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.factories.commands.create_shoot_command import ShootObjectCommandFactory
from src.infrastructure.factories.commands.macro.create_move_with_fuel_command import MoveWithFuelObjectCommandFactory
from src.infrastructure.factories.operation_router import OperationToCommandRouter
from src.infrastructure.factories.commands.macro import RotateWithVelocityCommandFactory


class StandardBattleRuleset(IRuleset):
    """
    Шаблон правил для стандартной космической битвы: 2 флотилии по 3 корабля, стрельба, движение, поворот.
    """

    def get_initial_objects(self) -> Dict[str, UObject]:
        """
        Создаёт 6 кораблей: 3 красных (fleet_red_0-2), 3 синих (fleet_blue_0-2).
        """
        objects = {}

        # Позиции и скорости условно расставлены
        red_positions = [Vector(-200, -100), Vector(-200, 0), Vector(-200, 100)]
        blue_positions = [Vector(200, -100), Vector(200, 0), Vector(200, 100)]

        for idx, position in enumerate(red_positions):
            obj_id = f"fleet_red_{idx}"
            objects[obj_id] = DictUObject({
                "position": position,
                "velocity": Vector(0, 0),
                "fuel_level": 1000,
                "fuel_consumption": 1,
                "angle": 0,
                "angular_velocity": 1,
                "directions_number": 8,
                "damage": 20,
                "range": 300,
                "can_shoot": True,
                "health_points": 100,
            })

        for idx, position in enumerate(blue_positions):
            obj_id = f"fleet_blue_{idx}"
            objects[obj_id] = DictUObject({
                "position": position,
                "velocity": Vector(0, 0),
                "fuel_level": 1000,
                "fuel_consumption": 1,
                "angle": 4,
                "angular_velocity": 1,
                "directions_number": 8,
                "damage": 20,
                "range": 300,
                "can_shoot": True,
                "health_points": 100,
            })

        return objects

    def get_allowed_operations(self) -> Dict[str, type[IObjectCommandFactory]]:
        return {
            "movement": MoveWithFuelObjectCommandFactory,
            "shoot": ShootObjectCommandFactory,
            "rotation": RotateWithVelocityCommandFactory,
        }

    def get_dependencies(self, game_id: str, session: GameSession) -> Dict[str, Callable[..., Any]]:
        router = OperationToCommandRouter(self.get_allowed_operations())
        dependencies = {
            'Game.Object.GetAll': lambda: session.get_all_objects(),
            'Game.Object.Get': lambda obj_id: session.get_object_by_id(obj_id),
            'OperationToCommandMap': lambda op_id: router.get_factory(op_id),
        }
        return dependencies
