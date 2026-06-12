"""Custom exceptions for Database."""

# Базовые исключения для БД
class DatabaseError(Exception):
    """Базовый класс для ошибок базы данных."""
    pass


# Исключения для работы с таблицами
class TableAlreadyExistsError(DatabaseError):
    """Ошибка: таблица уже существует."""
    pass


class TableNotFoundError(DatabaseError):
    """Ошибка: таблица не найдена."""
    pass


# Исключения для работы с записями
class MissingColumnError(DatabaseError):
    """Ошибка: отсутствует обязательное поле."""
    pass


class UnknownColumnError(DatabaseError):
    """Ошибка: неизвестное поле."""
    pass


class InvalidAgeError(DatabaseError):
    """Ошибка: некорректный возраст."""
    pass


class DuplicateIDError(DatabaseError):
    """Ошибка: дублирующийся ID."""
    pass


# Исключения для файловой БД
class InvalidStorageDataError(DatabaseError):
    """Ошибка: повреждённые данные в файле."""
    pass