from services import app_service as svc
from services.auth_service import authenticate, register
from repositories.repositories import roles, users


def ask(label): return input(label).strip()
def show_rows(repo):
    rows = repo.get_all()
    if not rows: print('Записей нет.'); return
    for obj in rows: print(obj)

def table_menu(title, repo, fields):
    while True:
        print(f'\n--- {title} ---\n1. Просмотр\n2. Добавить\n3. Изменить\n4. Удалить\n0. Назад')
        choice = ask('Выбор: ')
        try:
            if choice == '1': show_rows(repo)
            elif choice == '2':
                data = {f: ask(f'{f}: ') for f in fields}
                if 'tariff' in data or 'volume' in data or 'amount' in data: 
                    for f in ('tariff','volume','amount'):
                        if f in data: data[f] = float(data[f])
                for f in ('user_role','resident_id','service_id','accountant_id','payment_id','method_id','accrual_id'):
                    if f in data: data[f] = int(data[f])
                print('Создана запись с ID:', repo.create(**data))
            elif choice == '3':
                item_id = int(ask('ID записи: ')); data = {f: ask(f'Новое значение {f}: ') for f in fields}
                print('Изменено.' if repo.update(item_id, **data) else 'Запись не найдена.')
            elif choice == '4':
                print('Удалено.' if repo.delete(int(ask('ID записи: '))) else 'Запись не найдена.')
            elif choice == '0': break
            else: print('Нет такого пункта.')
        except (ValueError, TypeError) as e: print('Ошибка ввода:', e)
        except Exception as e: print('Операция не выполнена:', e)

def resident_menu(user):
    while True:
        print(f'\n=== Кабинет жильца: {user.full_name} ===\n1. Мои начисления\n2. Мои платежи\n0. Выход')
        c=ask('Выбор: ')
        if c=='1':
            for a in svc.accruals.get_all():
                if a.resident_id == user.user_id: print(a)
        elif c=='2':
            own={a.accrual_id for a in svc.accruals.get_all() if a.resident_id==user.user_id}
            for p in svc.payments.get_all():
                if p.accrual_id in own: print(p)
        elif c=='0': break

def staff_menu(user):
    while True:
        print('\n=== Рабочее меню ===')
        for i, title in enumerate(svc.REPOSITORIES,1): print(f'{i}. {title}')
        print('8. Начислить плату', '\n9. Зарегистрировать платёж', '\n10. Выдать квитанцию', '\n0. Выход')
        c=ask('Выбор: ')
        try:
            if c.isdigit() and 1 <= int(c) <= 7:
                title=list(svc.REPOSITORIES)[int(c)-1]; repo, fields=svc.REPOSITORIES[title]; table_menu(title,repo,fields)
            elif c=='8':
                print('ID начисления:', svc.create_accrual(ask('ID жильца: '),ask('ID услуги: '),user.user_id,ask('Период ГГГГ-ММ: '),ask('Объём: ')))
            elif c=='9': print('ID платежа:',svc.create_payment(ask('ID начисления: '),ask('ID способа оплаты: '),ask('Сумма: '),ask('Дата ГГГГ-ММ-ДД: ')))
            elif c=='10': print('ID квитанции:',svc.issue_receipt(ask('ID платежа: '),ask('Номер: '),ask('Дата ГГГГ-ММ-ДД: ')))
            elif c=='0': break
            else: print('Нет такого пункта.')
        except Exception as e: print('Ошибка:',e)

def main():
    while True:
        print('\n===== Система «Коммуналка» =====\n1. Войти\n2. Зарегистрировать жильца\n0. Завершить')
        c=ask('Выбор: ')
        try:
            if c=='1':
                user=authenticate(ask('Логин: '),ask('Пароль: '))
                if not user: print('Неверный логин или пароль.'); continue
                role=roles.get_by_id(user.user_role)
                if role and role.name.lower() in ('жилец','resident'): resident_menu(user)
                else: staff_menu(user)
            elif c=='2':
                print('Доступные роли:')
                for r in roles.get_all(): print(r.user_role_id, r.name)
                role_id=next((r.user_role_id for r in roles.get_all() if r.name.lower() in ('жилец','resident')),None)
                if role_id is None: raise ValueError('В справочнике не настроена роль «Жилец».')
                register(ask('Логин: '),ask('Пароль: '),ask('ФИО: '),ask('Адрес: '),role_id)
                print('Регистрация выполнена.')
            elif c=='0': break
        except Exception as e: print('Ошибка:',e)
