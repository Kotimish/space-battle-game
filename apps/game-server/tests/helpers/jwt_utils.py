from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

BASE_DIR = Path(__file__).resolve().parents[2]
PRIVATE_KEY_PATH = BASE_DIR / "test_keys" / "private.pem"
PUBLIC_KEY_PATH = BASE_DIR / "test_keys" / "public.pem"


def read_private_key():
    with open(PRIVATE_KEY_PATH, "r") as f:
        return f.read()


def create_test_token(game_id: str, user_id: str, expire_minutes: int = 60):
    payload = {
        "sub": user_id,
        "game_id": game_id,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    }
    private_key = read_private_key()
    return jwt.encode(payload, private_key, algorithm="RS256")
