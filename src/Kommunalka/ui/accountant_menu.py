from services.app_service import create_accrual, create_payment, issue_receipt
from ui.common import show_records

def accountant_menu(user):
    while True:
        print(f"\n===== МЕНЮ БУХГАЛТЕРА ({user.full_name}) =====")
        print("1. Просмотреть жильцов")
        print("2. Просмотреть услуги")
        print("3. Просмотреть начисления")
        print("4. Просмотреть платежи")
        print("5. Создать начисление")
        print("6. Зарегистрировать платёж")
        print("7. Выдать квитанцию")
        print("0. Выход в главное меню")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_records("Пользователи")

        elif choice == "2":
            show_records("Услуги")

        elif choice == "3":
            show_records("Начисления")

        elif choice == "4":
            show_records("Платежи")

        elif choice == "5":
            try:
                user_id = int(input("ID жильца: "))
                service_id = int(input("ID услуги: "))
                volume = float(input("Объём услуги: "))
                amount = float(input("Сумма начисления: "))
                period = input("Период (например 2025-01): ").strip()

                create_accrual(
                    user_id=user_id,
                    service_id=service_id,
                    amount=amount,
                    period=period,
                    accountant_id=user.id,
                    volume=volume
                )
                print("Начисление успешно создано.")
            except Exception as error:
                print("Ошибка:", error)

        elif choice == "6":
            try:
                user_id = int(input("ID жильца: "))
                accrual_id = int(input("ID начисления: "))
                amount = float(input("Сумма платежа: "))
                method_id = int(input("ID способа оплаты (1-Наличные, 2-Карта, 3-Перевод): "))

                create_payment(
                    user_id=user_id,
                    accrual_id=accrual_id,
                    amount=amount,
                    payment_method_id=method_id,
                    cashier_id=user.id
                )
                print("Платёж успешно зарегистрирован.")
            except Exception as error:
                print("Ошибка:", error)

        elif choice == "7":
            try:
                payment_id = int(input("ID платежа: "))
                issue_receipt(payment_id)
            except Exception as error:
                print("Ошибка:", error)

        elif choice == "0":
            break
        else:
            print("Неверный пункт меню.")
