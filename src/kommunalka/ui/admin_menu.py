from services.auth_service import register
from ui.common import show_records, read_int


def admin_menu(user):
    while True:
        print("\n===== МЕНЮ АДМИНИСТРАТОРА =====")
        print("1. Зарегистрировать пользователя")
        print("2. Просмотреть пользователей")
        print("3. Просмотреть роли")
        print("4. Просмотреть услуги")
        print("5. Просмотреть способы оплаты")
        print("6. Просмотреть начисления")
        print("7. Просмотреть платежи")
        print("8. Просмотреть квитанции")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            login = input("Логин: ")
            password = input("Пароль: ")
            full_name = input("ФИО: ")
            address = input("Адрес: ")

            print("0 — Жилец")
            print("1 — Бухгалтер")
            print("2 — Администратор")

            role_id = read_int("Роль: ")

            if role_id not in (0, 1, 2):
                print("Некорректная роль.")
                continue

            try:
                register(
                    login,
                    password,
                    full_name,
                    address,
                    role_id
                )
                print("Пользователь зарегистрирован.")
            except Exception as error:
                print("Ошибка:", error)

        elif choice == "2":
            show_records("Пользователи")

        elif choice == "3":
            show_records("Роли пользователей")

        elif choice == "4":
            show_records("Услуги")

        elif choice == "5":
            show_records("Способы оплаты")

        elif choice == "6":
            show_records("Начисления")

        elif choice == "7":
            show_records("Платежи")

        elif choice == "8":
            show_records("Квитанции")

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню.")
