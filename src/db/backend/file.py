import json
from pathlib import Path
from typing import Any
from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table


class FileDatabase(Database):
    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        path = self._get_table_path(table_name)
        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidStorageDataError("Файл содержит некорректный JSON") from e
        return self._deserialize_table(data)

    def _save_table(self, table_name: str, table: Table) -> None:
        path = self._get_table_path(table_name)
        with path.open("w", encoding="utf-8") as f:
            json.dump(self._serialize_table(table), f, ensure_ascii=False, indent=2)

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _serialize_table(self, table: Table) -> dict[str, Any]:
        return {"columns": list(table.columns), "records": [r.copy() for r in table.records]}

    def _deserialize_table(self, data: dict[str, Any]) -> Table:
        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError("Некорректная структура файла")
        return Table(tuple(data["columns"]), data.get("records", []))