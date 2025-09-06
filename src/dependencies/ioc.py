from typing import Any, Callable

import src.exceptions.ioc as exceptions
from src.interfaces.base_command import BaseCommand
from src.interfaces.resolve_dependency_strategy import IDependencyResolver


class UpdateResolveDependencyStrategyCommand(BaseCommand):
    """Команда обновления стратегии регистрации зависимостей в IoC-контейнере"""
    def __init__(self, strategy_updater: Callable[[IDependencyResolver], IDependencyResolver]):
        self.strategy_updater = strategy_updater

    def execute(self) -> None:
        new_strategy = self.strategy_updater(IoC.dependency_resolver)
        IoC.dependency_resolver = new_strategy


class DefaultDependencyResolver(IDependencyResolver):
    """Дефолтная стратегия разрешения зависимостей в IoC-контейнере"""
    def resolve(self, dependency: str, *args, **kwargs) -> Any:
        if dependency == 'IoC.UpdateResolveStrategy':
            return UpdateResolveDependencyStrategyCommand(*args, **kwargs)
        raise exceptions.DependencyNotFoundError(f"Dependency '{dependency}' not registered")


class IoC:
    """IoC-контейнер для разрешения зависимостей"""
    dependency_resolver: IDependencyResolver = DefaultDependencyResolver()

    @classmethod
    def resolve(cls, dependency_name: str, *args: Any, **kwargs: Any) -> Any:
        return cls.dependency_resolver.resolve(dependency_name, *args, **kwargs)
