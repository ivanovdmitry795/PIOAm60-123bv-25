"""Text user interface for database."""

from .backend.memory import create_record, select_record


def print_menu():
    print("\n=== База студентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи")
    print("0. Выход")


def add_student():
    print("\nДобавление студента")
    
    try:
        student_id = int(input("id: "))
        first_name = input("Имя: ").strip()
        second_name = input("Фамилия: ").strip()
        age = int(input("Возраст: "))
        sex = input("Пол (м/ж): ").strip()
        
        record = create_record(student_id, first_name, second_name, age, sex)
        print(f"✅ Добавлено: {record}")
        
    except ValueError as e:
        print(f"❌ Ошибка: {e}")


def show_all():
    print("\n=== Все студенты ===")
    records = select_record()
    
    if not records:
        print("Нет записей")
    else:
        for r in records:
            print(f"id:{r[0]}, {r[1]} {r[2]}, {r[3]} лет, {r[4]}")


def find_students():
    print("\n=== Поиск (Enter = пропустить) ===")
    
    try:
        id_input = input("id: ").strip()
        student_id = int(id_input) if id_input else None
        
        first_name = input("Имя: ").strip() or None
        second_name = input("Фамилия: ").strip() or None
        
        age_input = input("Возраст: ").strip()
        age = int(age_input) if age_input else None
        
        sex = input("Пол: ").strip() or None
        
        records = select_record(student_id, first_name, second_name, age, sex)
        
        if not records:
            print("Ничего не найдено")
        else:
            for r in records:
                print(f"id:{r[0]}, {r[1]} {r[2]}, {r[3]} лет, {r[4]}")
                
    except ValueError:
        print("❌ Ошибка ввода")


def run():
    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            add_student()
        elif choice == "2":
            show_all()
        elif choice == "3":
            find_students()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверная команда")
