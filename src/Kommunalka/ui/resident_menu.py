from repositories import accrual_repository, payment_repository, service_repository
from ui.common import show_records

def resident_menu(user):
    while True:
        print(f"\n===== ЛИЧНЫЙ КАБИНЕТ ЖИЛЬЦА ({user.full_name}) =====")
        print("1. Мои начисления")
        print("2. Мои платежи")
        print("3. Список услуг и тарифов")
        print("0. Выход в главное меню")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            accruals = accrual_repository.get_by_user(user.id)
            if not accruals:
                print("У вас пока нет начислений.")
            else:
                print(f"\n{'ID':<5} {'Услуга':<8} {'Объём':<10} {'Сумма':<12} {'Период':<12}")
                print("-" * 55)
                for a in accruals:
                    print(f"{a.id:<5} {a.service_id:<8} {a.volume or 0:<10.2f} {a.amount:<12.2f} {a.period:<12}")

        elif choice == "2":
            payments = payment_repository.get_by_user(user.id)
            if not payments:
                print("У вас пока нет платежей.")
            else:
                print(f"\n{'ID':<5} {'Сумма':<12} {'Дата'}")
                print("-" * 35)
                for p in payments:
                    print(f"{p.id:<5} {p.amount:<12.2f} {p.paid_at or ''}")

        elif choice == "3":
            show_records("Услуги")

        elif choice == "0":
            break
        else:
            print("Неверный пункт меню.")
