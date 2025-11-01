import asyncio
from concurrent.futures import Future

from fastapi import HTTPException
from fastapi.requests import Request

from src.dependencies.ioc import IoC
from src.services.game_manager import GameManager
from src.interfaces.base_command import BaseCommand


async def get_game_manager() -> GameManager:
    """
    Получение экземпляра менеджера игровых сессий из IoC-контейнера.

    Также устанавливает инфраструктурный скоуп через IoC для защиты от неявных сбросов скоупов
    :return: Менеджер игровых сессий - обработчиков команд
    """
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'infrastructure_scope').execute()
    return IoC[GameManager].resolve('Game.QueueManager')


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