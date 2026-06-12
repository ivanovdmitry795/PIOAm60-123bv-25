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