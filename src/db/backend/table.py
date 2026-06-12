"""Table class for database."""

from typing import Any
from .errors import MissingColumnError, UnknownColumnError, InvalidAgeError, DuplicateIDError


class Table:
    def __init__(self, columns: tuple[str, ...], records: list[dict[str, Any]] | None = None) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []
        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:
        """Добавляет запись с проверкой типов и ограничений."""
        # Проверка наличия всех колонок
        missing = [c for c in self.columns if c not in record]
        if missing:
            raise MissingColumnError(f"Отсутствует поле '{missing[0]}'")
        
        # Проверка лишних колонок
        extra = [c for c in record if c not in self.columns]
        if extra:
            raise UnknownColumnError(f"Поле '{extra[0]}' не определено")
        
        # Проверка student_id
        student_id = record.get("student_id")
        if student_id is not None:
            if not isinstance(student_id, int):
                raise ValueError("student_id должен быть целым числом")
            if student_id <= 0:
                raise ValueError("student_id должен быть положительным числом")
        
        # Проверка возраста
        age = record.get("age")
        if age is not None:
            if not isinstance(age, int):
                raise ValueError("Возраст должен быть целым числом")
            if age < 0:
                raise InvalidAgeError("Возраст не может быть отрицательным")
            if age > 150:
                raise ValueError("Возраст не может быть больше 150")
        
        # Проверка имени
        first_name = record.get("first_name")
        if first_name is not None and isinstance(first_name, str):
            if not first_name.strip():
                raise ValueError("Имя не может быть пустым")
        
        # Проверка фамилии
        second_name = record.get("second_name")
        if second_name is not None and isinstance(second_name, str):
            if not second_name.strip():
                raise ValueError("Фамилия не может быть пустой")
        
        # Проверка пола
        sex = record.get("sex")
        if sex is not None:
            if sex not in ["м", "ж", "M", "F"]:
                raise ValueError("Пол должен быть 'м' или 'ж'")
        
        # Проверка дубликата ID
        for existing in self.records:
            if existing.get("student_id") == student_id:
                raise DuplicateIDError(f"Студент с id={student_id} уже существует")
        
        self.records.append(record.copy())

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        unknown = [k for k in filters if k not in self.columns]
        if unknown:
            raise UnknownColumnError(f"Поле '{unknown[0]}' не определено")
        if not filters:
            return [r.copy() for r in self.records]
        result = []
        for r in self.records:
            if all(r.get(k) == v for k, v in filters.items()):
                result.append(r.copy())
        return result