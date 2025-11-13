from typing import Callable, Any

from src.interfaces.ruleset import IRuleset
from src.interfaces.uobject import UObject
from src.models.game_session import GameSession


class DefaultRuleset(IRuleset):
    def get_initial_objects(self) -> dict[str, UObject]:
        # Нет объектов по умолчанию
        return {}

    def get_allowed_operations(self) -> dict[str, type]:
        # Нет разрешённых операций
        return {}

    def get_dependencies(self, game_id: str, session: GameSession) -> dict[str, Callable[..., Any]]:
        # Минимальная регистрация: только доступ к объектам сессии
        dependencies = {
            'Game.Object.GetAll': lambda: session.get_all_objects(),
            'Game.Object.Get': lambda obj_id: session.get_object_by_id(obj_id),
        }
        return dependencies
