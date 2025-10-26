from fastapi import APIRouter

router = APIRouter(tags=['health'])


@router.get("/health/")
async def health_check():
    """
    Простая проверка работоспособности веб-приложения
    :return: Словарь с ключом "status": "ok", если сервер запушен.
    """
    return {"status": "ok"}
