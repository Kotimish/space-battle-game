import pytest

from src.commands.ioc_commands.init_container import InitContainerCommand
from src.commands.ioc_commands.reset_container import ResetContainerCommand


@pytest.fixture(autouse=True)
def ioc_container():
    InitContainerCommand().execute()
    yield
    ResetContainerCommand().execute()
