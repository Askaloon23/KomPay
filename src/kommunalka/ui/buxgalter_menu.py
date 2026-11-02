from services.app_service import (
    create_accrual,
    create_payment,
    issue_receipt
)

from ui.common import show_records, read_int


def accountant_menu(user):
    while True:
        print("\n===== МЕНЮ БУХГАЛТЕРА =====")
        print("1. Просмотреть жильцов")
        print("2. Просмотреть услуги")
        print("3. Просмотреть начисления")
        print("4. Просмотреть платежи")
        print("5. Создать начисление")
        print("6. Зарегистрировать платёж")
        print("7. Выдать квитанцию")
        print("0. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            show_records("Пользователи")

        elif choice == "2":
            show_records("Услуги")

        elif choice == "3":
            show_records("Начисления")

        elif choice == "4":
            show_records("Платежи")

        elif choice == "5":
            user_id = read_int("ID жильца: ")
            service_id = read_int("ID услуги: ")
            amount = input("Сумма: ")
            period = input("Период: ")

            if None in (user_id, service_id):
                continue

            try:
                create_accrual(
                    user_id=user_id,
                    service_id=service_id,
                    amount=float(amount.replace(",", ".")),
                    period=period,
                    accountant_id=user.id
                )
                print("Начисление создано.")
            except Exception as error:
                print("Ошибка:", error)

        elif choice == "6":
            user_id = read_int("ID жильца: ")
            accrual_id = read_int("ID начисления: ")
            amount = input("Сумма платежа: ")
            method_id = read_int("ID способа оплаты: ")

            if None in (user_id, accrual_id, method_id):
                continue

            try:
                create_payment(
                    user_id=user_id,
                    accrual_id=accrual_id,
                    amount=float(amount.replace(",", ".")),
                    payment_method_id=method_id,
                    cashier_id=user.id
                )
                print("Платёж зарегистрирован.")
            except Exception as error:
                print("Ошибка:", error)

        elif choice == "7":
            payment_id = read_int("ID платежа: ")

            if payment_id is not None:
                try:
                    issue_receipt(payment_id)
                    print("Квитанция оформлена.")
                except Exception as error:
                    print("Ошибка:", error)

        elif choice == "0":
            break

        else:
            print("Неверный пункт меню.")
