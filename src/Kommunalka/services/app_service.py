from repositories import user_repository, service_repository, accrual_repository, payment_repository

def create_accrual(user_id: int, service_id: int, amount: float, period: str,
                   accountant_id: int | None = None, volume: float | None = None) -> int:
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception("Жилец с таким ID не найден")
    if user.role_id != 3:
        raise Exception("Начисление можно создавать только для жильца")

    service = service_repository.get_by_id(service_id)
    if not service:
        raise Exception("Услуга с таким ID не найдена")

    if amount <= 0:
        raise Exception("Сумма начисления должна быть больше 0")

    return accrual_repository.create(
        user_id=user_id,
        service_id=service_id,
        amount=amount,
        period=period,
        accountant_id=accountant_id,
        volume=volume
    )

def create_payment(user_id: int, amount: float, accrual_id: int | None = None,
                   payment_method_id: int | None = None, cashier_id: int | None = None) -> int:
    user = user_repository.get_by_id(user_id)
    if not user:
        raise Exception("Жилец с таким ID не найден")

    if amount <= 0:
        raise Exception("Сумма платежа должна быть больше 0")

    if accrual_id:
        accrual = accrual_repository.get_by_id(accrual_id)
        if not accrual:
            raise Exception("Начисление с таким ID не найдено")

    return payment_repository.create(
        user_id=user_id,
        amount=amount,
        accrual_id=accrual_id,
        payment_method_id=payment_method_id,
        cashier_id=cashier_id
    )

def issue_receipt(payment_id: int) -> str:
    payment = payment_repository.get_by_id(payment_id)
    if not payment:
        raise Exception("Платёж с таким ID не найден")

    user = user_repository.get_by_id(payment.user_id)
    method_name = "Не указан"
    if payment.payment_method_id:
        # Простая заглушка названий
        methods = {1: "Наличные", 2: "Карта", 3: "Перевод"}
        method_name = methods.get(payment.payment_method_id, "Не указан")

    receipt = f"""
========== КВИТАНЦИЯ ==========
Номер платежа: {payment.id}
Жилец: {user.full_name if user else 'Неизвестен'}
Сумма: {payment.amount:.2f} руб.
Способ оплаты: {method_name}
Дата: {payment.paid_at}
===============================
"""
    print(receipt)
    return receipt
