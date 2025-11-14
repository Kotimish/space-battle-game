from src.infrastructure.dependencies.ioc import IoC
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.factories.object_command_factory import IObjectCommandFactory
from src.domain.interfaces.uobject import UObject
from src.domain.exceptions import game_object as object_exceptions
from src.application.schemas.agent_message import AgentMessage


class InterpretCommand(BaseCommand):
    """Команда интерпретации входящего сообщения"""
    def __init__(self, message: AgentMessage):
        self._message = message

    def execute(self) -> None:
        """
        Выполняет интерпретацию входящего сообщения агента
        :raises ObjectNotFoundError: если игровой объект с указанным object_id не найден
        """
        # Получаем хранилище игровых объектов
        game_object = IoC[UObject].resolve("Game.Object.Get", self._message.object_id)
        if game_object is None:
            raise object_exceptions.ObjectNotFoundError(f"Game object '{self._message.object_id}' does not exist.")
        # По названию операции получаем фабрику команды
        factory_class = IoC[type[IObjectCommandFactory]].resolve("OperationToCommandMap", self._message.operation_id)
        factory = factory_class()
        # Создаём и выполняем команду
        cmd = factory.create(game_object, self._message.arguments)
        cmd.execute()
