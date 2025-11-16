from concurrent.futures import ThreadPoolExecutor

import pytest

from src.infrastructure.dependencies.ioc import IoC


@pytest.mark.parametrize(
    'count_workers',
    [1, 2, 3]
)
def test_threads(count_workers):
    """Тест работы нескольких областей (scope) в разных потоках"""
    # Результаты разрешения зависимостей из разных потоков
    results = {}

    def worker_thread(idx: int):
        # Создаем новую область (scope) внутри потока
        IoC.resolve('IoC.Scope.Create', f'thread_{idx}').execute()
        IoC.resolve('IoC.Scope.Set', f'thread_{idx}').execute()
        # Регистрируем зависимость
        strategy = lambda: f'thread_{idx}_value'
        IoC.resolve('IoC.Register', f'thread_{idx}_strategy', strategy).execute()
        # Разрешаем зависимость
        result = IoC.resolve(f'thread_{idx}_strategy')
        results[idx] = result
        # Проверяем текущую область (scope) на зависимость
        assert IoC.resolve(f'thread_{idx}_strategy') == f'thread_{idx}_value'

    with ThreadPoolExecutor(max_workers=count_workers) as executor:
        futures = [
            executor.submit(worker_thread, thread_id)
            for thread_id in range(count_workers)
        ]
        for future in futures:
            future.result()

    for key, value in results.items():
        assert value == f'thread_{key}_value'
