from src.domain.interfaces.base_command import BaseCommand


class SoftStopCommand(BaseCommand):
    """Команда остановки цикла выполнения команд только после завершения их выполнения"""
    def __init__(self, *args, **kwargs):
        pass

    def execute(self) -> None:
        pass
