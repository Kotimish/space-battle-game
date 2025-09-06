from contextvars import ContextVar

from src.dependencies.scope import Scope
from src.interfaces.base_command import BaseCommand


class GetCurrentScopeCommand(BaseCommand):
    """Получить текущую активную область (scope)"""
    def __init__(self, current_scope: ContextVar[Scope | None], default_scope: Scope | None = None):
        self._current_scope = current_scope
        self._default_scope = default_scope

    def execute(self) -> str:
        scope = self._current_scope.get() or self._default_scope
        return scope.name
