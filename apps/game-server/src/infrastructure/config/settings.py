from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# game-server/src/infrastructure/config/settings.py
# game-server/ — корень микросервиса, содержит .env и .env.default
BASE_DIR = Path(__file__).resolve().parents[3]


class JwtConfig(BaseModel):
    """Настройки для JWT (путь к публичному ключу и алгоритм)."""
    public_key_path: Path
    algorithm: str = "RS256"


class GameServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GAME__",
        env_nested_delimiter="__",
        env_file=(
            BASE_DIR / ".env.default",
            BASE_DIR / ".env",
        ),
    )
    jwt: JwtConfig


settings = GameServerSettings()