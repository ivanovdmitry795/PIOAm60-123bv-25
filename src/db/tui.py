from src.db.backend.file import FileDatabase
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import TableNotFoundError, TableAlreadyExistsError


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
            exit()

    def _add_record(self):
        try:
            record = {
                "student_id": int(input("id: ")),
                "first_name": input("Имя: ").strip(),
                "second_name": input("Фамилия: ").strip(),
                "age": int(input("Возраст: ")),
                "sex": input("Пол (м/ж): ").strip(),
            }
            self.db.insert_record(self.current_table, record)
            print("✅ Добавлено!")
        except ValueError:
            print("❌ Ошибка ввода")

    def _show_all(self):
        records = self.db.select_records(self.current_table)
        if not records:
            print("Нет записей")
        else:
            for r in records:
                print(f"id:{r['student_id']}, {r['first_name']} {r['second_name']}, {r['age']} лет, {r['sex']}")

    def _find_records(self):
        filters = {}
        id_input = input("id (Enter пропустить): ").strip()
        if id_input:
            filters["student_id"] = int(id_input)
        name = input("Имя: ").strip()
        if name:
            filters["first_name"] = name
        records = self.db.select_records(self.current_table, **filters)
        if not records:
            print("Ничего не найдено")
        else:
            for r in records:
                print(f"id:{r['student_id']}, {r['first_name']} {r['second_name']}, {r['age']} лет, {r['sex']}")