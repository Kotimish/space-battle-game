from typing import Callable, Awaitable, Any

from fastapi import Request

from src.application.interfaces.jwt_service import IJWTService
from src.application.interfaces.middleware import IMiddleware
from src.domain.interfaces.base_command import BaseCommand
from src.infrastructure.dependencies.ioc import IoC
from src.infrastructure.exceptions import auth_middleware as exceptions


class AuthMiddleware(IMiddleware):
    """
    Middleware для проверки JWT-токена в защищённых эндпоинтах.
    """

    def __init__(self, protected_paths: list[tuple[str, set]]):
        """
        Инициализирует middleware списком защищённых маршрутов.
        :param protected_paths: Список кортежей (префикс пути, множество методов требующих аутентификации),
                                для которых обязательна JWT-аутентификация.
        """
        self.protected_paths = protected_paths

    def _is_path_protected(self, path: str, method: str) -> bool:
        """
        Проверяет, является ли указанный путь защищённым (требующим аутентификации)
        :param path: Путь входящего HTTP-запроса.
        :return: True, если путь начинается с любого из префиксов из protected_paths, иначе False.
        """
        for prefix, auth_required_methods in self.protected_paths:
            if path.startswith(prefix):
                # Если метод в списке методов, требующих аутентификации, возвращаем True
                return method.upper() in auth_required_methods
        # Если путь не начинается ни с одного из префиксов, доступ разрешён без аутентификации
        return False

    async def __call__(self, request: Request, call_next: Callable[[Request], Awaitable[Any]]):
        """
        Обрабатывает входящий запрос в цепочке middleware.

        Если путь запроса не входит в список защищённых — запрос немедленно
        передаётся следующему обработчику без проверки токена.
        :param request: Входящий HTTP-запрос.
        :param call_next: Функция для передачи запроса следующему middleware.
        :return: Ответ от последующих обработчиков.
        """
        if not self._is_path_protected(request.url.path, request.method):
            return await call_next(request)

        # Получаем JWT-сервис через IoC
        # Явная установка скоупа для разрешения зависимости
        IoC[BaseCommand].resolve('IoC.Scope.Set', 'infrastructure_scope').execute()
        jwt_service: IJWTService = IoC[IJWTService].resolve('JWTService')
        # Получаем токен
        token = await self._extract_token(request)

        # Декодируем и проверяем токен
        try:
            payload = jwt_service.decode(token)
        except Exception as exception:
            raise exceptions.InvalidTokenError(
                "Invalid token",
                status_code=401
            )

        # Бизнес-валидация
        body = await request.json()
        game_id_from_body = body.get("game_id")
        game_id_from_token = payload.get("game_id")

        user_id_from_body = body.get("user_id")
        user_id_from_token = payload.get("sub")

        # Запуск проверки только если нужное поле есть в теле запроса
        if game_id_from_body:
            if not game_id_from_token:
                raise exceptions.InvalidTokenError(
                    "Token missing 'game_id' claim",
                    status_code=401
                )

            if game_id_from_token != game_id_from_body:
                raise exceptions.InvalidTokenError(
                    "Token game_id does not match request game_id",
                    status_code=403
                )

        # Запуск проверки только если нужное поле есть в теле запроса
        if user_id_from_body:
            if not user_id_from_token:
                raise exceptions.InvalidTokenError(
                    "Token missing 'sub' claim",
                    status_code=401
                )

            if user_id_from_token != user_id_from_body:
                raise exceptions.InvalidTokenError(
                    "Token sub does not match request user_id",
                    status_code=403
                )

        return await call_next(request)

    async def _extract_token(self, request: Request) -> str:
        """
        Извлекает JWT-токен из заголовка Authorization.

        Ожидаемый формат заголовка: "Bearer <token>".
        :param request:  Входящий HTTP-запрос.
        :return: Валидный JWT-токен.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise exceptions.MissingTokenError(
                "Missing or invalid Authorization header",
                status_code=401
            )
        return auth_header[7:]
