import src.domain.exceptions.move as move
import src.application.exceptions.repeat as repeat
import src.domain.exceptions.rotate as rotate
from src.application.commands.log_exception_command import LogExceptionCommand
from src.application.commands.move import MoveCommand
from src.application.commands.repeat import RepeatCommand
from src.application.commands.rotate import RotateCommand
from src.domain.exceptions.base_exception import BaseGameException

MOVE_EXCEPTIONS = {
    move.MovementException: lambda cmd, exc: RepeatCommand(cmd),
    move.UndefinedPositionError: lambda cmd, exc: RepeatCommand(cmd),
    move.UndefinedVelocityError: lambda cmd, exc: RepeatCommand(cmd),
    move.UnchangeablePositionError: lambda cmd, exc: RepeatCommand(cmd),
}

ROTATE_EXCEPTIONS = {
    rotate.RotateException: lambda cmd, exc: RepeatCommand(cmd),
    rotate.UndefinedAngleError: lambda cmd, exc: RepeatCommand(cmd),
    rotate.UndefinedAngularVelocityError: lambda cmd, exc: RepeatCommand(cmd),
    rotate.UnchangeableAngleError: lambda cmd, exc: RepeatCommand(cmd),
}

REPEAT_EXCEPTIONS = {
    repeat.RepeatException: lambda cmd, exc: LogExceptionCommand(cmd, exc),
}
# Словарь словарей обработчиков
DEFAULT_HANDLERS = {
    MoveCommand: MOVE_EXCEPTIONS,
    RotateCommand: ROTATE_EXCEPTIONS,
    RepeatCommand: REPEAT_EXCEPTIONS,
}
# Словарь для команд без явно определенного исключения
DEFAULT_COMMANDS = {
    MoveCommand: lambda cmd, exc: RepeatCommand(cmd),
    RotateCommand: lambda cmd, exc: RepeatCommand(cmd),
    RepeatCommand: lambda cmd, exc: LogExceptionCommand(cmd, exc),
    # SecondRepeatCommand: lambda cmd, exc: LogExceptionCommand(cmd, exc),
}
# Словарь для исключений без явно определенной команды
DEFAULT_EXCEPTIONS = {
    BaseGameException: lambda cmd, exc: LogExceptionCommand(cmd, exc)
}
# Дефолтный обработчик для ситуации без явно определенных исключения и команды
DEFAULT_HANDLER = lambda cmd, exc: LogExceptionCommand(cmd, exc)
