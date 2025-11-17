from src.infrastructure.config.settings import settings, BASE_DIR
from src.infrastructure.security.jwt_service import PyJWTService
from src.infrastructure.security.key_loader import load_public_key


def setup_jwt_service() -> PyJWTService:
    primary_path = settings.jwt.public_key_path
    fallback_path = BASE_DIR / "test_keys" / "public.pem"

    public_key = load_public_key(primary_path, fallback_path)
    return PyJWTService(public_key=public_key, algorithm=settings.jwt.algorithm)
