from repositories import user_repository, service_repository, accrual_repository, payment_repository

def show_records(entity: str):
    print(f"\n----- {entity} -----")

    if entity == "Пользователи":
        users = user_repository.get_all()
        if not users:
            print("Нет записей.")
            return
        print(f"{'ID':<5} {'Логин':<15} {'ФИО':<30} {'Роль':<15} {'Адрес'}")
        print("-" * 90)
        roles = {1: "Бухгалтер", 2: "Администратор", 3: "Жилец"}
        for u in users:
            role_name = roles.get(u.role_id, "Неизвестно")
            print(f"{u.id:<5} {u.login:<15} {u.full_name:<30} {role_name:<15} {u.address or ''}")

    elif entity == "Услуги":
        services = service_repository.get_all()
        if not services:
            print("Нет записей.")
            return
        print(f"{'ID':<5} {'Название':<25} {'Ед.изм.':<10} {'Тариф'}")
        print("-" * 55)
        for s in services:
            print(f"{s.id:<5} {s.name:<25} {s.unit or '':<10} {s.tariff:.2f}")

    elif entity == "Начисления":
        accruals = accrual_repository.get_all()
        if not accruals:
            print("Нет записей.")
            return
        print(f"{'ID':<5} {'Жилец':<8} {'Услуга':<8} {'Объём':<10} {'Сумма':<12} {'Период':<12}")
        print("-" * 65)
        for a in accruals:
            print(f"{a.id:<5} {a.user_id:<8} {a.service_id:<8} {a.volume or 0:<10.2f} {a.amount:<12.2f} {a.period:<12}")

    elif entity == "Платежи":
        payments = payment_repository.get_all()
        if not payments:
            print("Нет записей.")
            return
        print(f"{'ID':<5} {'Жилец':<8} {'Начисл.':<8} {'Сумма':<12} {'Дата'}")
        print("-" * 50)
        for p in payments:
            print(f"{p.id:<5} {p.user_id:<8} {p.accrual_id or '-':<8} {p.amount:<12.2f} {p.paid_at or ''}")

    else:
        print("Неизвестный тип записей.")
