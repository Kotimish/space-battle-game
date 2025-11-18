from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi.testclient import TestClient

from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.uobject import UObject
from src.infrastructure.dependencies.ioc import IoC
from tests.helpers.jwt_utils import create_test_token


def set_infrastructure_scope():
    """
    Явно устанавливает скоуп 'infrastructure_scope', чтобы гарантировать,
    что разрешение зависимости происходит в правильном контексте (основной поток).
    """
    IoC[BaseCommand].resolve('IoC.Scope.Set', 'infrastructure_scope').execute()


def create_game_session(test_client: TestClient, game_type: str = "test") -> str:
    """
    Создаёт новую игровую сессию через API и возвращает её идентификатор.
    :param test_client: Клиент для обмена сообщений с тестируемым сервером
    :param game_type: Тип игры
    :return: Идентификатор игровой сессии
    """
    response = test_client.post(
        f'/api/games',
        json={"game_type": game_type}
    )
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
    response = test_client.delete(f'/api/games/{game_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'status' in data
    assert data['status'] == 'terminated'


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
    # Настройка скоупа
    set_infrastructure_scope()
    # Инициализация игровой сессии
    game_id = create_game_session(test_client)

    # Генерируем токен для этой сессии
    token = create_test_token(game_id=game_id, user_id="user_0")

    # Проверяем статус игровой сессии
    response = test_client.get(f'/api/games/{game_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['id'] == game_id
    # Проверяем игровые объекты
    response = test_client.get(f'/api/games/{game_id}/objects')
    data = response.json()
    assert len(data['objects']) == len(initial_game_objects.keys())
    for key in initial_game_objects.keys():
        assert (data['objects'][key]) == initial_game_objects[key]

    # Проверяем игровые объекты
    for object_id in initial_game_objects:
        init_data = initial_game_objects[object_id]
        expect_data = expected_game_objects[object_id]
        # Проверяем статус игрового объекта до изменения
        response = test_client.get(f'/api/games/{game_id}/objects/{object_id}')
        assert response.status_code == 200
        data = response.json()
        assert data == init_data

        # Проверяем интерпретацию команды
        response = test_client.post(
            f'/api/games/command',
            json={
                "game_id": game_id,
                "object_id": object_id,
                "operation_id": "movement",
                "arguments": {
                    'velocity': {"x": 10, "y": 0},
                },
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'accepted'

        # Проверяем запрос к игровому объекту
        response = test_client.get(f'/api/games/{game_id}/objects/{object_id}')
        assert response.status_code == 200
        data = response.json()
        assert data == expect_data

    # Проверяем статус игровой сессии после выполнения команд
    response = test_client.get(f'/api/games/{game_id}/objects')
    data = response.json()
    assert len(data['objects']) == len(expected_game_objects.keys())
    for key in initial_game_objects.keys():
        assert data['objects'][key] == expected_game_objects[key]

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
                initial_game_objects,
                expected_game_objects
            )
            for _ in range(count_workers)
        ]
        for future in futures:
            future.result()
