from src.exceptions.base_exception import BaseGameException


class IoCContainerException(BaseGameException):
    """Базовое исключение для ошибок работы ioc-контейнера"""


class ScopeNotFoundError(IoCContainerException):
    """Ошибка возникает, когда область (scope) с указанным именем не существует или не найдена."""


class DependencyNotFoundError(IoCContainerException):
    """Ошибка возникает, когда зависимость не зарегистрирована ни в одной доступной области (scope)."""


class ScopeAlreadyExistsError(IoCContainerException):
    """Ошибка возникает при попытке создать область (scope) с уже существующим именем."""


class DependencyAlreadyRegisteredError(IoCContainerException):
    """Ошибка возникает при попытке зарегистрировать уже существующую зависимость."""


class ForbiddenRegistrationDependencyError(IoCContainerException):
    """Ошибка возникает при попытке зарегистрировать зависимость в корневой области (root scope)."""


class ForbiddenRemoveRootScopeError(IoCContainerException):
    """Ошибка возникает при попытке удалить корневую область."""


class ForbiddenRemoveScopeError(IoCContainerException):
    """Ошибка возникает при попытке удалить область без родителя."""


class ParentScopeNotFoundError(IoCContainerException):
    """Ошибка возникает при попытке получить родительский элемент корневой области."""
