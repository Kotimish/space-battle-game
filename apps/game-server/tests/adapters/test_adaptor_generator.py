from abc import ABC, abstractmethod
from typing import Type

from src.infrastructure.factories.adaptor_factory import AdapterFactory
from src.infrastructure.dependencies.ioc import IoC
from src.domain.interfaces.base_command import BaseCommand
from src.domain.interfaces.uobject import UObject
from src.domain.models.uobject import DictUObject


class ITest(ABC):
    """Тестовый интерфейс"""

    @abstractmethod
    def get_test_value(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def set_test_value(self, test: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def sum(self, first_value: int, second_value: int) -> int:
        raise NotImplementedError


def test_adaptor_generator():
    """Тест получения класс-адаптера из генератора адаптеров"""
    # Получение фабрики адаптеров под интерфейс
    adapter_class = AdapterFactory.get_adapter(ITest)
    # Создание адаптера
    uobject: UObject = DictUObject()
    adapter = adapter_class(uobject)
    assert hasattr(adapter, 'get_test_value')
    assert hasattr(adapter, 'set_test_value')
    assert hasattr(adapter, 'sum')
    assert isinstance(adapter, ITest)


def test_adaptor_get_method():
    """Тест метода получения атрибута адаптера"""
    data = {
        'test_value': 'test'
    }
    # Получение фабрики адаптеров под интерфейс
    adapter_class = AdapterFactory.get_adapter(ITest)
    # регистрация зависимостей для адаптера
    get_factory = lambda obj, key, *args, **kwargs: obj.get_property(key)
    IoC[BaseCommand].resolve('IoC.Register', 'ITest:test_value.get', get_factory).execute()
    # Создание адаптера
    uobject = DictUObject(data)
    adapter = adapter_class(uobject)
    assert adapter.get_test_value() == data['test_value']


def test_adaptor_set_method():
    """Тест метода установки атрибута адаптера"""
    test_value = 'test'
    # Получение фабрики адаптеров под интерфейс
    adapter_class = AdapterFactory.get_adapter(ITest)
    # регистрация зависимостей для адаптера
    set_factory = lambda obj, key, value, *args, **kwargs: obj.set_property(key, value)
    IoC[BaseCommand].resolve('IoC.Register', 'ITest:test_value.set', set_factory).execute()
    get_factory = lambda obj, key, *args, **kwargs: obj.get_property(key)
    IoC[BaseCommand].resolve('IoC.Register', 'ITest:test_value.get', get_factory).execute()
    # Создание адаптера
    uobject = DictUObject()
    adapter = adapter_class(uobject)
    adapter.set_test_value(test_value)

    assert adapter.get_test_value() == test_value


def test_adapter_generic_method():
    """Тест нестандартного метода адаптера"""
    test_first_value = 10
    test_second_value = 15
    # Получение фабрики адаптеров под интерфейс
    adapter_class = AdapterFactory.get_adapter(ITest)
    # регистрация зависимостей для адаптера
    sum_factory = lambda first_value, second_value, *args, **kwargs: first_value + second_value
    IoC[BaseCommand].resolve('IoC.Register', 'ITest:sum', sum_factory).execute()
    # Создание адаптера
    uobject = DictUObject()
    adapter = adapter_class(uobject)

    assert adapter.sum(test_first_value, test_second_value) == test_first_value + test_second_value


def test_ioc_adapter():
    """Тест получения класса-адаптера через ioc-контейнер"""
    test_value = 'test'
    # регистрация зависимостей для адаптера
    set_factory = lambda obj, key, value, *args, **kwargs: obj.set_property(key, value)
    IoC[BaseCommand].resolve('IoC.Register', 'ITest:test_value.set', set_factory).execute()
    get_factory = lambda obj, key, *args, **kwargs: obj.get_property(key)
    IoC[BaseCommand].resolve('IoC.Register', 'ITest:test_value.get', get_factory).execute()
    # Получение фабрики адаптеров под интерфейс
    adapter_class = IoC[Type[ITest]].resolve('Adapter', ITest)
    # Создание адаптера
    uobject = DictUObject()
    adapter = adapter_class(uobject)

    assert isinstance(adapter, ITest)
    adapter.set_test_value(test_value)
    assert adapter.get_test_value() == test_value
