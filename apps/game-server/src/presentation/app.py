from fastapi import FastAPI

from src.presentation.api import router as api_router
from src.presentation.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
