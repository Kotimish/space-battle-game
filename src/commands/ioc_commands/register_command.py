from contextvars import ContextVar
from typing import Callable, Any

import src.exceptions.ioc as exceptions
from src.dependencies.scope import Scope
from src.interfaces.base_command import BaseCommand


class RegisterDependencyCommand(BaseCommand):
    """Команда регистрации новой зависимости в IoC-контейнере"""
    def __init__(self, current_scope: ContextVar[Scope | None], dependency: str, strategy: Callable[[list[Any]], Any]):
        self._current_scope = current_scope
        self._dependency = dependency
        self._strategy = strategy

    def execute(self) -> None:
        scope = self._current_scope.get()
        if scope is None:
            raise exceptions.ScopeNotFoundError(
                f'Current scope for dependency \'{self._dependency}\' registration not found'
            )
        if scope.is_default:
            raise exceptions.ForbiddenRegistrationDependencyError(
                f'Cannot register dependency \'{self._dependency}\' in root scope. '
                f'The root scope is reserved for internal IoC infrastructure'
            )
        if self._dependency in scope.dependencies:
            raise exceptions.DependencyAlreadyRegisteredError(
                f'There is already dependency registered with the name \'{self._dependency}\''
            )
        scope.dependencies[self._dependency] = self._strategy
