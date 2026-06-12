from typing import Any
from .errors import MissingColumnError, UnknownColumnError


class Table:
    def __init__(self, columns: tuple[str, ...], records: list[dict[str, Any]] | None = None) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []
        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:
        missing = [c for c in self.columns if c not in record]
        if missing:
            raise MissingColumnError(f"Отсутствует поле '{missing[0]}'")
        extra = [c for c in record if c not in self.columns]
        if extra:
            raise UnknownColumnError(f"Поле '{extra[0]}' не определено")
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