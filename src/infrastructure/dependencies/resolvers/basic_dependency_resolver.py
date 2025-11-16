from contextvars import ContextVar
from typing import Any

from src.infrastructure.dependencies.scope import Scope
import src.infrastructure.exceptions.ioc as exceptions
from src.infrastructure.interfaces.resolve_dependency_strategy import IDependencyResolver


class BasicDependencyResolver(IDependencyResolver):
    """Стратегия разрешения базовых зависимостей в IoC-контейнере"""
    def __init__(self, all_scopes: dict[str, Scope], current_scope: ContextVar[Scope | None], default_scope: Scope):
        self._all_scopes = all_scopes
        self._current_scope = current_scope
        self._default_scope = default_scope

    def resolve(self, dependency_name: str, *args, **kwargs) -> Any:
        scope = self._current_scope.get() or self._default_scope
        while scope:
            # Получение стратегии по названию
            strategy = scope.dependencies.get(dependency_name)
            if strategy:
                return strategy(*args, **kwargs)
            # Если стратегия не найдена, то ищем родителя
            scope = scope.parent
        raise exceptions.DependencyNotFoundError(f'Dependency \'{dependency_name}\' not registered')
