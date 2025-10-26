import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


def main():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
