from queue import Queue

from src.domain.interfaces.base_command import BaseCommand


class MoveToCommand(BaseCommand):
    """Команда перенаправления команд из очереди в другую очередь"""
    def __init__(self, target_queue: Queue["BaseCommand"]):
        self.target_queue = target_queue

    def execute(self) -> None:
        pass
