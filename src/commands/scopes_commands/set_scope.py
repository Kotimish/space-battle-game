from contextvars import ContextVar

from src.dependencies.scope import Scope
from src.exceptions.ioc import ScopeNotFoundError
from src.interfaces.base_command import BaseCommand


class SetScopeCommand(BaseCommand):
    """Попытка установить область (scope) в качестве активной"""
    def __init__(self, all_scopes: dict[str, Scope], current_scope: ContextVar[Scope | None], new_scope_name: str):
        self._all_scopes = all_scopes
        self._current_scope = current_scope
        self._new_scope_name = new_scope_name

    def execute(self) -> None:
        new_scope = self._all_scopes.get(self._new_scope_name)
        if new_scope is None:
            raise ScopeNotFoundError( f'Scope with name "{self._new_scope_name}" not found.')
        self._current_scope.set(new_scope)
