import pytest

from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.uobject import UObject
from src.domain.models.uobject import DictUObject
from src.domain.models.vector import Vector
from src.infrastructure.commands.ioc_commands.init_container import InitContainerCommand
from src.infrastructure.commands.ioc_commands.reset_container import ResetContainerCommand
from src.infrastructure.dependencies.ioc import IoC


@pytest.fixture
def game_objects() -> dict[str, UObject]:
    return {
        "object_0": DictUObject({
            "position": Vector(100, 0),
            "velocity": Vector(0, 0),
            "health_points": 100
        }),
    }


@pytest.fixture(autouse=True)
def ioc_container(game_objects):
    InitContainerCommand().execute()
    # Создание базового пространства
    IoC[BaseCommand].resolve('IoC.Scope.Create', 'base_game_scope').execute()
    # Установка базового пространства в качестве активного
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'base_game_scope').execute()
    # Регистрация объектов
    IoC[BaseCommand].resolve('IoC.Register', 'Game.Session.GetAll', lambda: game_objects).execute()
    yield
    ResetContainerCommand().execute()
