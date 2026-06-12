"""Text user interface for database."""

from src.db.backend.file import FileDatabase
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import (
    TableNotFoundError, 
    TableAlreadyExistsError,
    InvalidAgeError,
    DuplicateIDError,
    MissingColumnError,
    UnknownColumnError
)


class TUI:
    def __init__(self):
        print("\n=== Выбор типа базы данных ===")
        print("1. In-memory (данные не сохраняются)")
        print("2. File database (данные сохраняются)")
        choice = input("Выберите (1 или 2): ")

        if choice == "2":
            self.db = FileDatabase()
            print("✅ Файловая БД (папка 'data/')")
        else:
            self.db = MemoryDatabase()
            print("✅ In-memory БД")

        self.current_table = None

    def run(self):
        while True:
            if self.current_table is None:
                self._table_menu()
            else:
                self._record_menu()

    def _table_menu(self):
        print("\n=== Управление таблицами ===")
        print("1. Создать таблицу студентов")
        print("2. Выбрать таблицу")
        print("0. Выход")

        choice = input("Выберите: ")

        if choice == "1":
            try:
                self.db.create_table("students", ("student_id", "first_name", "second_name", "age", "sex"))
                self.current_table = "students"
                print("✅ Таблица создана!")
            except TableAlreadyExistsError as e:
                print(f"❌ {e}")
                self.current_table = "students"
        elif choice == "2":
            try:
                self.db._load_table("students")
                self.current_table = "students"
                print("✅ Таблица загружена!")
            except TableNotFoundError:
                print("❌ Таблица не найдена. Создайте её.")
        elif choice == "0":
            print("До свидания!")
            exit()

    def _record_menu(self):
        print(f"\n=== Таблица: {self.current_table} ===")
        print("1. Добавить запись")
        print("2. Показать все")
        print("3. Найти")
        print("4. Назад")
        print("0. Выход")

        choice = input("Выберите: ")

        if choice == "1":
            self._add_record()
        elif choice == "2":
            self._show_all()
        elif choice == "3":
            self._find_records()
        elif choice == "4":
            self.current_table = None
        elif choice == "0":
            print("До свидания!")
            exit()
        else:
            print("❌ Неверная команда")

    def _add_record(self):
        """Добавление новой записи с проверками."""
        print("\n=== Добавление студента ===")
        
        try:
            # Ввод ID
            student_id = input("id: ").strip()
            if not student_id:
                print("❌ Ошибка: id не может быть пустым")
                return
            try:
                student_id = int(student_id)
            except ValueError:
                print("❌ Ошибка: id должен быть целым числом")
                return
            
            # Ввод имени
            first_name = input("Имя: ").strip()
            if not first_name:
                print("❌ Ошибка: имя не может быть пустым")
                return
            
            # Ввод фамилии
            second_name = input("Фамилия: ").strip()
            if not second_name:
                print("❌ Ошибка: фамилия не может быть пустой")
                return
            
            # Ввод возраста
            age = input("Возраст: ").strip()
            if not age:
                print("❌ Ошибка: возраст не может быть пустым")
                return
            try:
                age = int(age)
            except ValueError:
                print("❌ Ошибка: возраст должен быть целым числом")
                return
            
            # Ввод пола
            sex = input("Пол (м/ж): ").strip()
            if not sex:
                print("❌ Ошибка: пол не может быть пустым")
                return
            if sex.lower() not in ["м", "ж"]:
                print("❌ Ошибка: пол должен быть 'м' или 'ж'")
                return
            
            # Создание записи
            record = {
                "student_id": student_id,
                "first_name": first_name,
                "second_name": second_name,
                "age": age,
                "sex": sex.lower(),
            }
            self.db.insert_record(self.current_table, record)
            print(f"✅ Добавлено: {record}")
            
        except InvalidAgeError as e:
            print(f"❌ Ошибка возраста: {e}")
        except DuplicateIDError as e:
            print(f"❌ Ошибка: {e}")
        except (MissingColumnError, UnknownColumnError) as e:
            print(f"❌ Ошибка структуры: {e}")
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {e}")

    def _show_all(self):
        """Показать все записи."""
        print("\n=== Все студенты ===")
        try:
            records = self.db.select_records(self.current_table)
            if not records:
                print("Нет записей")
            else:
                print(f"Всего записей: {len(records)}")
                for r in records:
                    print(f"id:{r['student_id']}, {r['first_name']} {r['second_name']}, {r['age']} лет, {r['sex']}")
        except TableNotFoundError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def _find_records(self):
        """Поиск записей с фильтрацией и проверкой ввода."""
        print("\n=== Поиск (Enter = пропустить) ===")
        
        filters = {}
        
        # Ввод ID с проверкой
        id_input = input("id (Enter пропустить): ").strip()
        if id_input:
            try:
                filters["student_id"] = int(id_input)
            except ValueError:
                print("❌ Ошибка: id должен быть целым числом")
                return
        
        # Ввод имени
        first_name = input("Имя: ").strip()
        if first_name:
            filters["first_name"] = first_name
        
        # Ввод фамилии
        second_name = input("Фамилия: ").strip()
        if second_name:
            filters["second_name"] = second_name
        
        # Ввод возраста с проверкой
        age_input = input("Возраст (Enter пропустить): ").strip()
        if age_input:
            try:
                filters["age"] = int(age_input)
            except ValueError:
                print("❌ Ошибка: возраст должен быть целым числом")
                return
        
        # Ввод пола
        sex = input("Пол (м/ж): ").strip()
        if sex:
            if sex.lower() not in ["м", "ж"]:
                print("❌ Ошибка: пол должен быть 'м' или 'ж'")
                return
            filters["sex"] = sex.lower()
        
        # Поиск
        try:
            records = self.db.select_records(self.current_table, **filters)
            if not records:
                print("Ничего не найдено")
            else:
                print(f"\nНайдено {len(records)} записей:")
                for r in records:
                    print(f"id:{r['student_id']}, {r['first_name']} {r['second_name']}, {r['age']} лет, {r['sex']}")
        except TableNotFoundError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Ошибка поиска: {e}")