from contextvars import ContextVar

from src.infrastructure.dependencies.scope import Scope
from src.domain.interfaces.base_command import BaseCommand


class ResetScopeCommand(BaseCommand):
    """Удаление всех пользовательских областей (scope) кроме корневой (root scope)"""
    def __init__(self, all_scopes: dict[str, Scope], current_scope: ContextVar[Scope | None]):
        self._all_scopes = all_scopes
        self._current_scope = current_scope

    def execute(self) -> None:
        root_scope = self._all_scopes.get('root')
        self._all_scopes.clear()
        self._all_scopes[root_scope.name] = root_scope
        self._current_scope.set(root_scope)
