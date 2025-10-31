import copy
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock

from src.adapters.move_fuel_consumer_adapter import MoveFuelConsumer
from src.commands.macro.move_with_fuel_command import MoveWithFuelCommand
from src.dependencies.ioc import IoC
from src.factories.commands.create_move_with_fuel_command import MoveWithFuelCommandFactory
from src.factories.operation_router import OperationToCommandRouter
from src.game_manager import GameManager
from src.interfaces.base_command import BaseCommand
from src.interfaces.uobject import UObject
from src.main import app
from src.models.uobject import DictUObject
from src.models.vector import Vector


def get_game_manager() -> GameManager:
    """
    Получение через IoC-контейнер менеджера игровых сессий.

    Явно устанавливает скоуп 'infrastructure_scope', чтобы гарантировать,
    что разрешение зависимости происходит в правильном контексте (основной поток).
    :return: Менеджер управления игровых сессий - обработчиков команд
    """
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'infrastructure_scope').execute()
    return IoC[GameManager].resolve('Game.QueueManager')


@pytest.fixture
def test_client():
    """
    Тестовый клиент для обмена сообщений с тестируемым сервером.
    По умолчанию использует lifespan веб-фреймворка FastApi.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture
def initial_game_objects() -> dict[str, UObject]:
    """
    Предоставляет начальное состояние игровых объектов для тестов.
    """
    return {
        'game_0': DictUObject({
            'position': Vector(0, 0),
            'velocity': Vector(10, 0),
            'fuel_level': 100,
            'fuel_consumption': 10,
        })
    }


@pytest.fixture
def expected_game_objects() -> dict[str, UObject]:
    """
    Предоставляет ожидаемое состояние игровых объектов после выполнения команды.
    """
    return {
        'game_0': DictUObject({
            'position': Vector(10, 0),
            'velocity': Vector(10, 0),
            'fuel_level': 0,
            'fuel_consumption': 10,
        })
    }


def create_game_session(test_client: TestClient) -> str:
    """
    Создаёт новую игровую сессию через API и возвращает её идентификатор.
    :param test_client: Клиент для обмена сообщений с тестируемым сервером
    :return: Идентификатор игровой сессии
    """
    response = test_client.post(f'/games')
    assert response.status_code == 200
    data = response.json()
    assert 'game_id' in data
    return data['game_id']


def delete_game_session(test_client: TestClient, game_id: str) -> None:
    """
    Завершает игровую сессию через API и проверяет корректность ответа.
    :param test_client: Клиент для обмена сообщений с тестируемым сервером
    :param game_id: Идентификатор игровой сессии
    """
    # Удаляем игровую сессию
    response = test_client.delete(
        f'/games/{game_id}'
    )
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert data['status'] == 'terminated'


def init_dependencies(game_id: str, initial_game_objects: dict[str, UObject]) -> None:
    """
    Регистрирует тестовые зависимости в скоупе игровой сессии через очередь команд.
    :param game_id: Идентификатор игровой сессии
    :param initial_game_objects: Входные тестовые данные
    """
    # Получаем игровую сессию - обработчик команд
    game_manager: GameManager = get_game_manager()
    handler = game_manager.get(game_id)
    # Регистрация зависимостей
    # -- Хранилище игровых объектов--
    # Получение всех объектов
    get_all_object_command = IoC[BaseCommand].resolve(
        'IoC.Register',
        'Game.Object.GetAll',
        lambda *args, **kwargs: initial_game_objects
    )
    # Получение объекта по id
    get_object_command = IoC[BaseCommand].resolve(
        'IoC.Register',
        'Game.Object.Get',
        lambda game_id, *args, **kwargs: initial_game_objects.get(game_id)
    )
    # -- Команды --
    move_command = IoC[BaseCommand].resolve(
        'IoC.Register',
        'Command.MoveWithFuel',
        lambda uobject, *args, **kwargs: MoveWithFuelCommand(MoveFuelConsumer(uobject))
    )
    # -- Разрешенные команды через роутер фабрик --
    allowed_operations = {
        'movement': MoveWithFuelCommandFactory,
    }
    factories = OperationToCommandRouter(allowed_operations)
    allowed_operations_command = IoC[BaseCommand].resolve(
        'IoC.Register',
        'OperationToCommandMap',
        lambda key, *args, **kwargs: factories.get_factory(key)
    )
    # Вспомогательная команда для ожидания выполнения очереди
    event = threading.Event()
    mock_command = Mock()
    mock_command.execute = lambda: event.set()
    # Добавление команд в очередь
    commands = [
        get_all_object_command,
        get_object_command,
        move_command,
        allowed_operations_command,
        mock_command
    ]
    for command in commands:
        handler.enqueue_command(command)
    # Ожидаем регистрации всех зависимостей
    event.wait()


def endpoint_worker(
        test_client: TestClient,
        initial_game_objects: dict[str, UObject],
        expected_game_objects: dict[str, UObject],
):
    """
    Выполняет полный сценарий взаимодействия с игровым сервером в отдельном потоке.

    Сценарий:
    1. Создаёт игровую сессию.
    2. Регистрирует тестовые зависимости в новом скоупе.
    3. Проверяет начальное состояние объектов.
    4. Отправляет команду 'movement' через endpoint `/game/command`.
    5. Проверяет, что состояние объекта изменилось в соответствии с ожиданиями.
    6. Завершает сессию.

    :param test_client: Клиент для обмена сообщений с тестируемым сервером
    :param initial_game_objects: Входные тестовые данные
    :param expected_game_objects: Ожидаемые тестовые данные
    """
    # Инициализация игровой сессии
    game_id = create_game_session(test_client)
    # Регистрируем зависимости в очереди игровой сессии
    init_dependencies(game_id, initial_game_objects)

    # Проверяем получение статуса игровой сессии и всех объектов в ней
    response = test_client.get(
        f'/games/{game_id}'
    )
    assert response.status_code == 200
    data = response.json()
    assert 'game_id' in data
    assert data['game_id'] == game_id
    assert 'objects' in data
    assert len(data['objects']) == len(initial_game_objects.keys())
    for key in initial_game_objects.keys():
        assert data['objects'][key] == initial_game_objects[key].to_dict()

    # Проверяем игровые объекты
    for object_id in initial_game_objects:
        init_data = initial_game_objects[object_id]
        expect_data = expected_game_objects[object_id]
        # Проверяем статус игрового объекта до изменения
        response = test_client.get(
            f'/games/{game_id}/objects/{object_id}'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['object'] == init_data.to_dict()

        # Проверяем интерпретацию команды
        response = test_client.post(
            f'/games/command',
            json={
                "game_id": game_id,
                "object_id": object_id,
                "operation_id": "movement",
                "arguments": {
                    'velocity': {"x": 10, "y": 0},
                },
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'accepted'

        # Проверяем запрос к игровому объекту
        response = test_client.get(
            f'/games/{game_id}/objects/{object_id}'
        )
        assert response.status_code == 200
        data = response.json()

        assert 'object' in data
        assert data['object'] == expect_data.to_dict()

    # Проверяем статус игровой сессии после выполнения команд
    response = test_client.get(
        f'/games/{game_id}'
    )
    assert response.status_code == 200
    data = response.json()
    assert 'game_id' in data
    assert data['game_id'] == game_id
    assert 'objects' in data
    assert len(data['objects']) == len(expected_game_objects.keys())
    for key in initial_game_objects.keys():
        assert data['objects'][key] == expected_game_objects[key].to_dict()

    # Завершение игровой сессии
    delete_game_session(test_client, game_id)


@pytest.mark.parametrize(
    'count_workers',
    [1, 2, 3]
)
def test_several_sessions(
    count_workers: int,
    test_client: TestClient,
    initial_game_objects: dict[str, UObject],
    expected_game_objects: dict[str, UObject],
):
    """
    Проверяет корректность работы API при параллельной обработке нескольких сессий.

    Запускает указанное число потоков, каждый из которых выполняет
    полный сценарий тестирования с изолированной игровой сессией.
    Использует глубокое копирование для предотвращения гонок данных между потоками.

    :param count_workers: Число потоков
    :param test_client: Клиент для обмена сообщений с тестируемым сервером
    :param initial_game_objects: Входные тестовые данные
    :param expected_game_objects: Ожидаемые тестовые данные
    """
    with ThreadPoolExecutor(max_workers=count_workers) as executor:
        futures = [
            executor.submit(
                endpoint_worker,
                test_client,
                # Полная копия для защиты от изменений
                copy.deepcopy(initial_game_objects),
                expected_game_objects
            )
            for _ in range(count_workers)
        ]
        for future in futures:
            future.result()
