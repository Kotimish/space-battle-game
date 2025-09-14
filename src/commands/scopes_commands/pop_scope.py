from contextvars import ContextVar

import src.exceptions.ioc as exceptions
from src.dependencies.ioc import IoC
from src.dependencies.scope import Scope
from src.interfaces.base_command import BaseCommand


class PopScopeCommand(BaseCommand):
    """
    Удаление текущей области (scope) и установка родительской в качестве активной области
    """
    def __init__(self, all_scopes: dict[str, Scope], current_scope: ContextVar[Scope | None]):
        self._all_scopes = all_scopes
        self._current_scope = current_scope

    def execute(self) -> str:
        scope = self._current_scope.get()
        if scope.is_default:
            raise exceptions.ForbiddenRemoveRootScopeError('The root scope cannot be removed')
        try:
            parent_name = IoC.resolve('IoC.Scope.Parent').execute()
        except exceptions.ParentScopeNotFoundError:
            raise exceptions.ForbiddenRemoveScopeError('The scope without parent cannot be removed')
        parent = self._all_scopes.get(parent_name)
        self._current_scope.set(parent)
        deleted_scope = self._all_scopes.pop(scope.name)
        return deleted_scope.name
