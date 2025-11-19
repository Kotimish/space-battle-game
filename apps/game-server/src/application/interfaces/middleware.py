from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable
# TODO В идеале заменить
from fastapi import Request


class IMiddleware(ABC):
    @abstractmethod
    async def __call__(
            self,
            request: Request,
            call_next: Callable[[Request], Awaitable[Any]]
    ) -> Any:
        raise NotImplementedError
