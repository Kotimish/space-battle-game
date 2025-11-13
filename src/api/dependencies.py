import asyncio
from concurrent.futures import Future

from fastapi import HTTPException

from src.dependencies.ioc import IoC
from src.interfaces.base_command import BaseCommand
from src.interfaces.serializers.uobject_serializer import IGameObjectSerializer
from src.services.game_service import GameService


def get_game_service() -> GameService:
    """
    Получение через IoC-контейнер сервиса игровых сессий.

    Явно устанавливает скоуп 'infrastructure_scope', чтобы гарантировать,
    что разрешение зависимости происходит в правильном контексте (основной поток).
    :return: Менеджер управления игровых сессий - обработчиков команд
    """
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'infrastructure_scope').execute()
    return IoC[GameService].resolve('GameService')


def get_serializer() -> IGameObjectSerializer:
    """
    Получение через IoC-контейнер сериализатора игровых сессий.
    :return: Класс сериализации/десериализации
    """
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'infrastructure_scope').execute()
    return IoC[IGameObjectSerializer].resolve('GameObjectSerializer')


async def wait_for_threaded_future(future: Future, timeout: float):
    """
    Вспомогательный метод для ожидания результата асинхронной операции, выполняемой в отдельном потоке.

    Функция позволяет асинхронно дождаться завершения синхронной или блокирующей операции,
    не останавливая основной (асинхронный) цикл событий.
    :param future: Объект Future - результат операции, выполняемой в рабочем потоке
    :param timeout: Максимальное время ожидания результата в секундах
    :return: Некое значение, возвращённое целевой функцией, связанной с Future
    """
    loop = asyncio.get_running_loop()
    try:
        return await asyncio.wait_for(
            loop.run_in_executor(None, future.result, None),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise HTTPException(504, "Game state request timed out")