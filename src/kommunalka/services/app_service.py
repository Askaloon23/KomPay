from repositories.repositories import (users, roles, services, methods, accruals, payments, receipts)
from services.auth_service import register

REPOSITORIES = {
 'Роли пользователей': (roles, ('name',)),
 'Услуги': (services, ('name','unit','tariff')),
 'Способы оплаты': (methods, ('name',)),
 'Пользователи': (users, ('login','password','full_name','address','user_role')),
 'Начисления': (accruals, ('resident_id','service_id','accountant_id','period','volume','amount')),
 'Платежи': (payments, ('accrual_id','method_id','amount','payment_date','status')),
 'Квитанции': (receipts, ('payment_id','number','issue_date')),
}

def create_accrual(resident_id, service_id, accountant_id, period, volume):
    resident = users.get_by_id(int(resident_id)); accountant = users.get_by_id(int(accountant_id))
    service = services.get_by_id(int(service_id))
    if not resident: raise ValueError('Жилец не найден.')
    if not accountant: raise ValueError('Бухгалтер не найден.')
    if not service: raise ValueError('Услуга не найдена.')
    if len(period) != 7 or period[4] != '-' or not period[:4].isdigit() or not period[5:].isdigit():
        raise ValueError('Период должен иметь формат ГГГГ-ММ.')
    if not 1 <= int(period[5:]) <= 12: raise ValueError('Месяц должен быть от 01 до 12.')
    volume = float(volume)
    if volume <= 0: raise ValueError('Объём должен быть больше нуля.')
    amount = round(volume * float(service.tariff), 2)
    return accruals.create(resident_id=int(resident_id), service_id=int(service_id),
        accountant_id=int(accountant_id), period=period, volume=volume, amount=amount)

def create_payment(accrual_id, method_id, amount, payment_date):
    a = accruals.get_by_id(int(accrual_id)); m = methods.get_by_id(int(method_id))
    if not a: raise ValueError('Начисление не найдено.')
    if not m: raise ValueError('Способ оплаты не найден.')
    amount = float(amount)
    if amount <= 0 or amount > float(a.amount): raise ValueError('Сумма должна быть больше нуля и не превышать начисление.')
    return payments.create(accrual_id=int(accrual_id), method_id=int(method_id), amount=amount,
                           payment_date=payment_date, status='confirmed')

def issue_receipt(payment_id, number, issue_date):
    if not payments.get_by_id(int(payment_id)): raise ValueError('Платёж не найден.')
    if not number.strip(): raise ValueError('Номер квитанции обязателен.')
    return receipts.create(payment_id=int(payment_id), number=number.strip(), issue_date=issue_date)
