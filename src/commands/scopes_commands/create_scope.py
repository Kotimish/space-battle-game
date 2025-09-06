from contextvars import ContextVar

import src.exceptions.ioc as exceptions
from src.commands.scopes_commands.get_parent_scope import GetParentScopeCommand
from src.dependencies.ioc import IoC
from src.dependencies.scope import Scope
from src.interfaces.base_command import BaseCommand


class CreateScopeCommand(BaseCommand):
    """Создание новой области (scope)"""
    def __init__(self, all_scopes: dict[str, Scope], current_scope: ContextVar[Scope | None], name: str):
        self._all_scopes = all_scopes
        self._parent = current_scope.get()
        self._name = name

    def execute(self) -> str:
        if self._name in self._all_scopes:
            raise exceptions.ScopeAlreadyExistsError(f'There is already scope registered with the name {self._name}')
        new_scope = Scope(self._name, {})
        if not self._parent:
            parent_name = IoC.resolve('IoC.Scope.Current').execute()
            self._parent = self._all_scopes.get(parent_name)
        new_scope.parent = self._parent
        new_scope.dependencies["IoC.Scope.Parent"] = lambda *args, **kwargs: GetParentScopeCommand(new_scope.parent)
        self._all_scopes[new_scope.name] = new_scope
        return new_scope.name
