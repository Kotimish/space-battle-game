import inspect
from types import NoneType
from typing import Callable, Any, Type, TypeVar, get_type_hints

from src.dependencies.ioc import IoC
from src.interfaces.uobject import UObject

T = TypeVar('T')


class AdapterFactory:
    """Фабрика создания адаптеров по интерфейсу"""
    adapter_cache: dict[str, Any] = {}

    @classmethod
    def get_adapter(cls, interface_class: Type[T]) -> Type[T]:
        """Получение класса-адаптера на основе интерфейса"""
        if interface_class.__name__ not in cls.adapter_cache:
            cls.adapter_cache[interface_class.__name__] = cls.generate_adapter(interface_class)
        return cls.adapter_cache[interface_class.__name__]

    @classmethod
    def generate_adapter(cls, interface_class: Type[T]) -> Type[T]:
        """Создание класса-адаптера на основе интерфейса"""
        if interface_class.__name__.startswith('I'):
            class_name = f"{interface_class.__name__[1:]}Adapter"
        else:
            class_name = f"{interface_class.__name__}Adapter"

        adapter_class = type(
            class_name,
            (interface_class,),
            {
                'obj': UObject,
                '__init__': cls._generate_constructor(),
                **cls._generate_methods(interface_class)
            }
        )
        return adapter_class

    @classmethod
    def _generate_constructor(cls) -> Callable[[Any, Any], None]:
        """Создание инициализирующего конструктора"""

        def __init__(self, obj: UObject):
            self.obj = obj

        return __init__

    @classmethod
    def _generate_methods(cls, interface_class) -> dict[str, Callable[..., Any]]:
        """Создание методов на основе интерфейсов"""
        methods = {}
        for method_name, method in inspect.getmembers(interface_class, predicate=inspect.isfunction):
            if method_name.startswith('__'):
                continue
            if hasattr(method, '__isabstractmethod__') and method.__isabstractmethod__:
                methods[method_name] = cls._generate_method(
                    interface_class.__name__,
                    method_name,
                    method
                )
        return methods

    @classmethod
    def _generate_method(cls, interface_name: str, method_name: str, method: Callable[..., Any]) -> Callable[..., Any]:
        """Создание метода на основе метода интерфейса"""
        return_type = cls._get_method_return_type(method)
        param_types = cls._get_method_params(method)
        if method_name.startswith('set') and return_type is NoneType and len(param_types) == 1:
            method = cls._generate_setter_method(interface_name, method_name, param_types)
        elif method_name.startswith('get') and return_type is not NoneType and len(param_types) == 0:
            method = cls._generate_getter_method(interface_name, method_name, return_type)
        else:
            method = cls._generate_generic_method(interface_name, method)
        return method

    @classmethod
    def _generate_getter_method(cls, interface_name: str, method_name: str, return_type: Any) -> Callable[[Any], Any]:
        """Создание метода получения атрибута"""
        property_name = cls._extract_property_name(method_name, 'get')
        key = cls._generate_command_key(interface_name, property_name, 'get')

        def getter_method(self):
            return IoC.resolve(key, self.obj, property_name)

        getter_method.__name__ = method_name
        getter_method.__annotations__ = {'return': return_type}
        return getter_method

    @classmethod
    def _generate_setter_method(cls, interface_name: str, method_name: str, param_types: dict[str, Any]) -> Callable[
        [Any, Any], Any]:
        """Создание метода установки атрибута"""
        property_name = cls._extract_property_name(method_name, 'set')
        key = cls._generate_command_key(interface_name, property_name, 'set')
        value_type = next(iter(param_types.values()), None)

        def setter_method(self, value):
            IoC.resolve(key, self.obj, property_name, value)

        setter_method.__name__ = method_name
        setter_method.__annotations__ = {'value': value_type, 'return': None}
        return setter_method

    @classmethod
    def _generate_generic_method(cls, interface_name: str, method: Callable[..., Any]) -> Callable[[Any, Any], Any]:
        """Создание общего метода, который не подходит под получение или установку атрибута"""
        key = f'{interface_name}:{method.__name__}'
        return_type = cls._get_method_return_type(method)

        def generic_method_with_return(self, *args, **kwargs):
            return IoC.resolve(key, *args, **kwargs)

        def generic_method_without_return(self, *args, **kwargs):
            IoC.resolve(key, *args, **kwargs)

        if return_type is NoneType:
            generic_method = generic_method_without_return
        else:
            generic_method = generic_method_with_return

        generic_method.__name__ = method.__name__
        generic_method.__annotations__ = get_type_hints(method)
        return generic_method

    @staticmethod
    def _extract_property_name(method_name: str, prefix: str = None) -> str:
        """Парсинг названия атрибута в имени функции"""
        if prefix and method_name.startswith(prefix):
            method_name = method_name[len(prefix):]
            if method_name.startswith('_'):
                method_name = method_name[1:]
        # Если первая и вторая буква заглавные,
        # то это указатель на аббревиатуру и оставляем как есть
        if len(method_name) > 1 and method_name[0].isupper() and method_name[1].isupper():
            return method_name
        if method_name and method_name[0].isupper():
            return method_name[0].lower() + method_name[1:]

        return method_name

    @staticmethod
    def _get_method_return_type(method: Callable[..., Any]) -> Any | None:
        """Получает тип возвращаемого значения из аннотаций метода"""
        hints = get_type_hints(method)
        return hints.get('return', NoneType)

    @staticmethod
    def _get_method_params(method: Callable[..., Any]):
        """Получает типы параметров из аннотаций метода"""
        hints = get_type_hints(method)
        return {
            key: value
            for key, value in hints.items()
            if key != 'return'
        }

    @staticmethod
    def _generate_command_key(interface_name: str, property_name: str, operation: str) -> str:
        return f"{interface_name}:{property_name}.{operation}"
