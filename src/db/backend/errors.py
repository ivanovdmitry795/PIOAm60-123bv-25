"""Custom exceptions for StudentTable."""

class StudentTableError(Exception):
    """Базовый класс для ошибок таблицы Student."""
    pass

class InvalidAgeError(StudentTableError):
    """Ошибка: некорректный возраст."""
    pass

class DuplicateIDError(StudentTableError):
    """Ошибка: дублирующийся ID."""
    pass

class DatabaseError(Exception):
    """Базовый класс для ошибок базы данных."""
    pass

class TableAlreadyExistsError(DatabaseError):
    """Ошибка: таблица уже существует."""
    pass

class TableNotFoundError(DatabaseError):
    """Ошибка: таблица не найдена."""
    pass

class MissingColumnError(DatabaseError):
    """Ошибка: отсутствует обязательное поле."""
    pass

class UnknownColumnError(DatabaseError):
    """Ошибка: неизвестное поле."""
    pass

class InvalidStorageDataError(DatabaseError):
    """Ошибка: повреждённые данные в файле."""
    pass