from typing import List


class AuthGameSession:
    def __init__(self, game_id: str, participants: List[str]):
        self.game_id = game_id
        self.participants = set(participants)
