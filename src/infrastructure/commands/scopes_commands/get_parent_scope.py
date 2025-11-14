from src.infrastructure.dependencies.scope import Scope
from src.infrastructure.exceptions import ioc as exceptions
from src.domain.interfaces.base_command import BaseCommand


class GetParentScopeCommand(BaseCommand):
    """Получение родительской области (scope) у текущей"""
    def __init__(self, parent: Scope | None = None):
        self._parent = parent

    def execute(self) -> str:
        if self._parent:
            return self._parent.name
        raise exceptions.ParentScopeNotFoundError('The root scope has no a parent scope.')
