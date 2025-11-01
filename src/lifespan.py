from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.commands.ioc_commands.init_container import InitContainerCommand
from src.commands.ioc_commands.reset_container import ResetContainerCommand
from src.dependencies.ioc import IoC
from src.services.game_manager import GameManager
from src.interfaces.base_command import BaseCommand


def setup_game_manager() -> GameManager:
    """
    Инициализирует менеджер игровых сессий и регистрирует его в IoC-контейнере.
    """
    game_manager = GameManager()
    # Регистрация менеджера игровых сессий в IoC
    IoC[BaseCommand].resolve('IoC.Register', 'Game.QueueManager', lambda: game_manager).execute()
    # Регистрация методов менеджера игровых сессий в IoC
    IoC[BaseCommand].resolve('IoC.Register', 'Game.Queue.Get', lambda game_id: game_manager.get(game_id)).execute()
    IoC[BaseCommand].resolve('IoC.Register', 'Game.Queue.Create', lambda: game_manager.create()).execute()
    IoC[BaseCommand].resolve('IoC.Register', 'Game.Queue.Stop', lambda game_id: game_manager.stop_game(game_id)).execute()
    IoC[BaseCommand].resolve('IoC.Register', 'Game.Queue.StopAll', lambda: game_manager.stop_all_games()).execute()
    return game_manager


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
    game_manager = setup_game_manager()
    yield
    # Остановка всех игровых сессий
    game_manager.stop_all_games()
    # Сброс скоупов
    IoC[BaseCommand].resolve('IoC.Scope.Reset').execute()
    # Сброс IoC-контейнера
    ResetContainerCommand().execute()