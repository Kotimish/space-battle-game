import logging
from typing import Callable, Awaitable, Any

from fastapi import Request

from src.application.interfaces.middleware import IMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(IMiddleware):
    """
    Middleware для логирования входящих запросов и исходящих ответов.
    """

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Any]]):
        """
        Обрабатывает входящий запрос и логирует его параметры до передачи
        следующему middleware или эндпоинту.

        :param request: Входящий HTTP-запрос от клиента.
        :param call_next: Функция для передачи запроса по цепочке middleware.
        :return: Ответ от последующих обработчиков (обычно Response).
        """
        try:
            body = await request.json()
        except Exception as e:
            # Тело может отсутствовать или быть не JSON
            logger.debug("Request body is missing or not valid JSON: %s", str(e))
            body = None

        # Логирование входящего запроса
        logger.info(
            "Incoming request: %s %s",
            request.method,
            request.url.path,
        )
        logger.debug(
            "Request details: headers=%s, body=%s",
            dict(request.headers),
            body,
        )

        # Выполняем следующий обработчик
        response = await call_next(request)

        # Логирование ответа (если это Response)
        if hasattr(response, 'status_code') and hasattr(response, 'headers'):
            logger.info(
                "Outgoing response: status=%s",
                response.status_code,
            )
            logger.debug(
                "Response details: headers=%s",
                dict(response.headers),
            )

        return response
