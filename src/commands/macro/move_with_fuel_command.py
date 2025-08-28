from src.commands.fuel_command import CheckFuelCommand, BurnFuelCommand
from src.commands.macro.macro_command import MacroCommand
from src.commands.move import MoveCommand
from src.interfaces.move_fuel_consumer import IMoveFuelConsumer


class MoveWithFuelCommand(MacroCommand):
    """Макро-Команда движения по прямой с расходом топлива"""
    def __init__(self, movable: IMoveFuelConsumer):
        self._movable = movable
        self._commands = [
            CheckFuelCommand(movable),
            MoveCommand(movable),
            BurnFuelCommand(movable),
        ]
        super().__init__(self._commands)
