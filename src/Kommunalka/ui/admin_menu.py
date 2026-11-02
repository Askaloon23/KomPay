from services.auth_service import register
from ui.common import show_records

def admin_menu(user):
    while True:
        print(f"\n===== МЕНЮ АДМИНИСТРАТОРА ({user.full_name}) =====")
        print("1. Просмотреть всех пользователей")
        print("2. Создать бухгалтера")
        print("3. Создать администратора")
        print("4. Просмотреть услуги")
        print("5. Просмотреть начисления")
        print("6. Просмотреть платежи")
        print("0. Выход в главное меню")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_records("Пользователи")

        elif choice == "2":
            _create_staff(1, "Бухгалтер")

        elif choice == "3":
            _create_staff(2, "Администратор")

        elif choice == "4":
            show_records("Услуги")

        elif choice == "5":
            show_records("Начисления")

        elif choice == "6":
            show_records("Платежи")

        elif choice == "0":
            break
        else:
            print("Неверный пункт меню.")

def _create_staff(role_id: int, role_name: str):
    print(f"\n--- Создание {role_name.lower()}а ---")
    login = input("Логин: ").strip()
    password = input("Пароль: ").strip()
    full_name = input("ФИО: ").strip()
    address = input("Адрес: ").strip()

    try:
        register(login, password, full_name, address, role_id)
        print(f"{role_name} успешно создан!")
    except Exception as e:
        print("Ошибка:", e)
