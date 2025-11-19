from typing import List
from  datetime import datetime, timezone

class AuthGameSession:
    def __init__(
        self,
        game_id: str,
        organizer_id: str,
        participants: List[str],
        created_at: datetime = None
    ):
        self.game_id = game_id
        self.organizer_id=organizer_id,
        self.participants = set(participants)
        self.created_at = created_at or datetime.now(timezone.utc)
