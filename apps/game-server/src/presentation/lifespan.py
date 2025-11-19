from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.domain.interfaces.base_command import BaseCommand
from src.infrastructure.commands.ioc_commands.init_container import InitContainerCommand
from src.infrastructure.commands.ioc_commands.reset_container import ResetContainerCommand
from src.infrastructure.dependencies.ioc import IoC
from src.infrastructure.setup.setup_game_service import setup_game_service
from src.infrastructure.setup.setup_jwt_service import setup_jwt_service
from src.infrastructure.setup.setup_logging import setup_logging
from src.infrastructure.setup.setup_serializer import setup_serializer


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

    # Настройка GameManager
    game_service = setup_game_service()
    # Настройка сервиса сериализатора
    serializer = setup_serializer()
    # Настройка сервиса JWT
    jwt_service = setup_jwt_service()
    # Настройка логгирования
    # setup_logging()

    # --- Регистрация зависимостей ---
    # Регистрация менеджера игровых сессий в IoC
    IoC[BaseCommand].resolve('IoC.Register', 'GameService', lambda: game_service).execute()
    # Регистрация сериализатора
    IoC[BaseCommand].resolve('IoC.Register', 'GameObjectSerializer', lambda: serializer).execute()
    # Регистрация сервиса JWT
    IoC[BaseCommand].resolve('IoC.Register', 'JWTService', lambda: jwt_service).execute()
    # -------

    yield

    # Остановка всех игровых сессий
    game_service.stop_all_game()
    # Сброс скоупов
    IoC[BaseCommand].resolve('IoC.Scope.Reset').execute()
    # Сброс IoC-контейнера
    ResetContainerCommand().execute()
