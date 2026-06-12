"""File-based database implementation using JSON."""

import json
from pathlib import Path
from typing import Any

from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table


class FileDatabase(Database):
    """База данных, хранящая таблицы в JSON-файлах."""

    def __init__(self, directory: str = "data") -> None:
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        """Загружает таблицу из файла с обработкой ошибок."""
        path = self._get_table_path(table_name)
        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidStorageDataError("Файл содержит некорректный JSON") from e
        except PermissionError as e:
            raise InvalidStorageDataError(f"Нет прав для чтения файла: {path}") from e
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка при чтении файла {path}: {e}") from e
        except Exception as e:
            raise InvalidStorageDataError(f"Неизвестная ошибка при загрузке: {e}") from e
        
        return self._deserialize_table(data)

    def _save_table(self, table_name: str, table: Table) -> None:
        """Сохраняет таблицу в файл с обработкой ошибок."""
        path = self._get_table_path(table_name)
        try:
            with path.open("w", encoding="utf-8") as f:
                json.dump(self._serialize_table(table), f, ensure_ascii=False, indent=2)
        except PermissionError as e:
            raise InvalidStorageDataError(f"Нет прав для записи файла: {path}") from e
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка при записи файла {path}: {e}") from e
        except Exception as e:
            raise InvalidStorageDataError(f"Неизвестная ошибка при сохранении: {e}") from e

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _serialize_table(self, table: Table) -> dict[str, Any]:
        return {"columns": list(table.columns), "records": [r.copy() for r in table.records]}

    def _deserialize_table(self, data: dict[str, Any]) -> Table:
        # Проверка наличия ключей
        if "columns" not in data:
            raise InvalidStorageDataError("Файл таблицы не содержит ключ 'columns'")
        if "records" not in data:
            raise InvalidStorageDataError("Файл таблицы не содержит ключ 'records'")
        
        # Проверка типа columns
        if not isinstance(data["columns"], list):
            raise InvalidStorageDataError(f"Поле 'columns' должно быть списком, получен {type(data['columns']).__name__}")
        
        # Проверка типа records
        if not isinstance(data["records"], list):
            raise InvalidStorageDataError(f"Поле 'records' должно быть списком, получен {type(data['records']).__name__}")
        
        # Проверка, что все элементы columns - строки
        for i, col in enumerate(data["columns"]):
            if not isinstance(col, str):
                raise InvalidStorageDataError(f"Элемент {i} в 'columns' должен быть строкой, получен {type(col).__name__}")
        
        # Проверка, что records - список словарей
        for i, record in enumerate(data["records"]):
            if not isinstance(record, dict):
                raise InvalidStorageDataError(f"Запись {i} должна быть словарём, получен {type(record).__name__}")
        
        return Table(tuple(data["columns"]), data["records"])