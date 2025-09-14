from src.dependencies.ioc import IoC, DefaultDependencyResolver, UpdateResolveDependencyStrategyCommand
from src.interfaces.base_command import BaseCommand


class ResetContainerCommand(BaseCommand):
    """Команда сброса IoC-контейнера в виде переназначения дефолтной стратегии"""

    def execute(self) -> None:
        IoC.resolve('IoC.Scope.Reset').execute()

        updater = lambda old_strategy: DefaultDependencyResolver()
        update_command = UpdateResolveDependencyStrategyCommand(updater)
        update_command.execute()
