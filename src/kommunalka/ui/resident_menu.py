from ui.common import show_records_for_user


def resident_menu(user):
    while True:
        print("\n===== ЛИЧНЫЙ КАБИНЕТ ЖИЛЬЦА =====")
        print("1. Мои начисления")
        print("2. Мои платежи")
        print("3. Мои квитанции")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_records_for_user(
                "Начисления",
                user.id
            )

        elif choice == "2":
            show_records_for_user(
                "Платежи",
                user.id
            )

        elif choice == "3":
            show_records_for_user(
                "Квитанции",
                user.id
            )

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню.")
