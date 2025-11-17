from datetime import datetime

from pydantic import BaseModel


class TokenResponse(BaseModel):
    game_id: str
    user_id: str
    access_token: str
    expires_at: datetime
