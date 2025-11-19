import logging
from typing import List

from fastapi import Request
from fastapi.responses import JSONResponse

from src.application.interfaces.middleware import IMiddleware
from src.domain.exceptions.base_exception import BaseGameException


class MiddlewareOrchestrator(IMiddleware):
    """
    Оркестратор цепочки middleware, реализующий паттерн «Цепочка обязанностей».

    Объединяет список middleware в единую цепочку выполнения, обеспечивая централизованную обработку ошибок.
    Каждый middleware вызывается в обратном порядке, заданном при инициализации
    (обратный порядок сборки цепочки, как в FastAPI).

    Все исключения, наследуемые от BaseGameException, преобразуются в JSON-ответ с соответствующим HTTP-статусом.
    Непредвиденные исключения обрабатываются как внутренние ошибки сервера (код 500).

    :param middlewares: Список middleware, участвующих в цепочке.
    """

    def __init__(self, middlewares: List[IMiddleware]):
        self.middlewares = middlewares

    async def __call__(self, request: Request, call_next):
        """
        Выполняет цепочку middleware и обрабатывает исключения.

        Собирает цепочку обработчиков от последнего к первому, после чего
        вызывает её с переданным запросом. Обеспечивает единый механизм
        обработки ошибок для всех middleware в цепочке.

        :param request: Входящий HTTP-запрос.
        :param call_next: Функция, вызывающая следующий обработчик в цепочке.
        :returns: HTTP-ответ, сформированный цепочкой middleware или эндпоинтом.
        """
        # Явное построение цепочки итеративно (от последнего к первому)
        handler = call_next
        for middleware in reversed(self.middlewares):
            handler = self._wrap(middleware, handler)

        try:
            return await handler(request)
        except BaseGameException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.message})
        except Exception as exception:
            logging.warning(exception)
            return JSONResponse(status_code=500, content={"detail": "Internal server error"})

    def _wrap(self, middleware: IMiddleware, next_handler):
        """
        Оборачивает middleware в совместимую функцию-обработчик.

        Создаёт замыкание, связывающее текущий middleware с обработчиком
        следующего шага (next_handler), чтобы обеспечить совместимость
        с интерфейсом call_next(request).

        :param middleware: Middleware для обработки запроса.
        :param next_handler: Следующий обработчик в цепочке.
        :returns: Асинхронная функция, принимающая Request и возвращающая Response.
        """

        async def wrapped(request: Request):
            return await middleware(request, next_handler)

        return wrapped
