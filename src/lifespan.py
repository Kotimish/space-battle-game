from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.commands.ioc_commands.init_container import InitContainerCommand
from src.commands.ioc_commands.reset_container import ResetContainerCommand
from src.dependencies.ioc import IoC
from src.executors.command_executor import CommandExecutor
from src.factories.command_handler.threaded_command_handler_factory import ThreadedCommandHandlerFactory
from src.factories.game_session_factory import GameSessionFactory
from src.interfaces.base_command import BaseCommand
from src.models.angle import Angle
from src.models.vector import Vector
from src.repositories.game_session_repository import InMemoryGameSessionRepository
from src.rules import DefaultRuleset, TestRuleset
from src.services.game_service import GameService
from src.services.ruleset_resolver import RulesetResolver
from src.services.serializers.dict_uobject_serializer import DictUObjectSerializer
from src.services.serializers.type_registry import TypeRegistry


def setup_game_service() -> GameService:
    """
    Инициализирует менеджер игровых сессий и регистрирует его в IoC-контейнере.
    """
    # Создание репозитория
    session_repository = InMemoryGameSessionRepository()
    # Создание обработчика очереди команд
    command_handler_factory = ThreadedCommandHandlerFactory()
    # Создание разрешителя правил
    rulesets = {
        "default": DefaultRuleset(),
        "test": TestRuleset(),
    }
    ruleset_resolver = RulesetResolver(rulesets)
    command_executor = CommandExecutor(session_repository, command_handler_factory, ruleset_resolver)
    session_factory = GameSessionFactory()
    # Создание основного сервис для работы с игровой сессией
    game_service = GameService(command_executor, session_repository, session_factory)

    # Регистрация сериализуемых типов
    type_registry = TypeRegistry()
    type_registry.register("Vector", Vector)
    type_registry.register("Angle", Angle)
    serializer = DictUObjectSerializer(type_registry.get_registry())

    # --- Регистрация зависимостей ---
    # Регистрация репозитория
    IoC[BaseCommand].resolve('IoC.Register', 'GameSessionRepository', lambda: session_repository).execute()
    # Регистрация менеджера игровых сессий в IoC
    IoC[BaseCommand].resolve('IoC.Register', 'GameService', lambda: game_service).execute()
    # Регистрация сериализатора
    IoC[BaseCommand].resolve('IoC.Register', 'GameObjectSerializer', lambda: serializer).execute()
    # ---

    return game_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения: инициализация и очистка ресурсов.

    При запуске (setup):
    1. Инициализирует глобальный IoC-контейнер.
    2. Создаёт и активирует инфраструктурный скоуп (`infrastructure_scope`),
       в котором регистрируются долгоживущие сервисы.
    3. Инициализирует и регистрирует долгоживущие сервисы в IoC.

    При завершении работы (shutdown):
    1. Останавливает все активные игровые сессии.
    2. Сбрасывает текущий скоуп и возвращает IoC к базовому состоянию.
    3. Полностью сбрасывает IoC-контейнер для предотвращения утечек состояния.
    """
    # Инициализация IoC-контейнера и базового скоупа
    InitContainerCommand().execute()
    # Создание инфраструктурного скоупа
    scope_name = 'infrastructure_scope'
    IoC[BaseCommand].resolve('IoC.Scope.Create', scope_name).execute()
    IoC[BaseCommand].resolve('IoC.Scope.Set', scope_name).execute()

    # Регистрация GameManager
    game_service = setup_game_service()
    yield
    # Остановка всех игровых сессий
    game_service.stop_all_game()
    # Сброс скоупов
    IoC[BaseCommand].resolve('IoC.Scope.Reset').execute()
    # Сброс IoC-контейнера
    ResetContainerCommand().execute()
