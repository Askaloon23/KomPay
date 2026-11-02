from services.auth_service import authenticate, register
from ui.admin_menu import admin_menu
from ui.accountant_menu import accountant_menu
from ui.resident_menu import resident_menu

def main():
    while True:
        print("\n========= СИСТЕМА УПРАВЛЕНИЯ ЖКХ =========")
        print("1. Войти")
        print("2. Зарегистрировать жильца")
        print("0. Выход")

        choice = input("Выбор: ").strip()

        if choice == "1":
            login = input("Логин: ").strip()
            password = input("Пароль: ").strip()

            user = authenticate(login, password)

            if user is None:
                print("Неверный логин или пароль!")
                continue

            print(f"\nДобро пожаловать, {user.full_name}!")

            if user.role_id == 2:          # Администратор
                admin_menu(user)
            elif user.role_id == 1:        # Бухгалтер
                accountant_menu(user)
            elif user.role_id == 3:        # Жилец
                resident_menu(user)
            else:
                print("Неизвестная роль пользователя")

        elif choice == "2":
            print("\n--- Регистрация жильца ---")
            login = input("Логин: ").strip()
            password = input("Пароль: ").strip()
            full_name = input("ФИО: ").strip()
            address = input("Адрес: ").strip()

            try:
                register(login, password, full_name, address, role_id=3)
                print("Жилец успешно зарегистрирован!")
            except Exception as e:
                print("Ошибка:", e)

        elif choice == "0":
            print("Выход из системы.")
            break

        else:
            print("Неверный пункт меню.")
