from fastapi import FastAPI

from src.infrastructure.middleware.auth_middleware import AuthMiddleware
from src.presentation.api import router as api_router
from src.presentation.lifespan import lifespan
from src.presentation.middleware import MiddlewareOrchestrator

app = FastAPI(lifespan=lifespan)

# Регистрация роутеров
app.include_router(api_router)

# Регистрация middleware
middlewares = [
    AuthMiddleware(protected_paths=["/api/games/command"]),
]
app.middleware("http")(MiddlewareOrchestrator(middlewares))