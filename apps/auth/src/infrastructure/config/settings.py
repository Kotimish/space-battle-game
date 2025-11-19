from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# auth/src/infrastructure/config/settings.py
# auth/ — корень микросервиса, содержит .env и .env.default
BASE_DIR = Path(__file__).resolve().parents[3]


class JwtConfig(BaseModel):
    """Настройки для JWT (путь к приватному ключу и алгоритм)."""
    private_key_path: Path
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH__",
        env_nested_delimiter="__",
        env_file=(
            BASE_DIR / ".env.default",
            BASE_DIR / ".env",
        ),
    )

    jwt: JwtConfig


settings = AuthSettings()
