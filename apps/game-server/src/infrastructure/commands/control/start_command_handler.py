from src.domain.interfaces.base_command import BaseCommand


class RunCommand(BaseCommand):
    """Команда запуска event-loop"""
    def __init__(self, *args, **kwargs):
        pass

    def execute(self) -> None:
        pass
