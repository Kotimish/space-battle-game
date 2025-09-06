import threading
from contextvars import ContextVar

from src.commands.ioc_commands.register_command import RegisterDependencyCommand
from src.commands.scopes_commands import (
    set_scope,
    reset_scope,
    get_current_scope,
    get_parent_scope,
    create_scope,
    pop_scope
)
from src.dependencies.ioc import IoC
from src.dependencies.resolvers.basic_dependency_resolver import BasicDependencyResolver
from src.dependencies.scope import Scope
from src.interfaces.base_command import BaseCommand


class InitContainerCommand(BaseCommand):
    """Инициализация глобального IoC-контейнера"""
    _all_scopes: dict[str, Scope] = {}
    _root_scope: Scope = None
    _current_scope: ContextVar[Scope | None] = ContextVar('_current_scope', default=_root_scope)

    def __init__(self):
        self._root_scope = Scope("root", {})
        self._root_scope.is_default = True
        # Регистрируем корневую область (root scope)
        self._all_scopes[self._root_scope.name] = self._root_scope
        # Устанавливаем корневую область в качестве активной
        self._current_scope.set(self._root_scope)

        self._already_executes_successfully: bool = False
        self._lock = threading.Lock()

    def execute(self) -> None:
        if self._already_executes_successfully:
            return
        with self._lock:
            # Список мета-зависимостей
            default_dependencies = {
                # Команда регистрации
                'IoC.Register': lambda *args, **kwargs: RegisterDependencyCommand(self._current_scope, *args, **kwargs),
                # Команды Scope
                'IoC.Scope.Set': lambda *args, **kwargs: set_scope.SetScopeCommand(self._all_scopes, self._current_scope, *args, **kwargs),
                'IoC.Scope.Pop': lambda *args, **kwargs: pop_scope.PopScopeCommand(self._all_scopes, self._current_scope),
                'IoC.Scope.Reset': lambda *args, **kwargs: reset_scope.ResetScopeCommand(self._all_scopes, self._current_scope),
                'IoC.Scope.Current': lambda *args, **kwargs: get_current_scope.GetCurrentScopeCommand(self._current_scope, self._root_scope),
                'IoC.Scope.Parent': lambda *args, **kwargs: get_parent_scope.GetParentScopeCommand(),
                'IoC.Scope.Create': lambda *args, **kwargs: create_scope.CreateScopeCommand(self._all_scopes, self._current_scope, *args, **kwargs)
            }
            # Регистрация дефолтных команд в корневом пространстве
            self._root_scope.dependencies.update(default_dependencies)

            update_command = IoC.resolve(
                'IoC.UpdateResolveStrategy',
                lambda old_strategy: BasicDependencyResolver(self._all_scopes, self._current_scope, self._root_scope)
            )
            update_command.execute()

            self._already_executes_successfully = True
