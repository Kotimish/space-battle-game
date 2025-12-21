from src.domain.interfaces.base_command import BaseCommand


class HardStopCommand(BaseCommand):
    """Команда остановки цикла выполнения команд не дожидаясь их полного завершения"""
    def __init__(self, *args, **kwargs):
        pass

    def execute(self) -> None:
        pass
