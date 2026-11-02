from database.init_db import initialize
from services.auth_service import register

initialize()

print("=== Создание сотрудников ===")
print("\n1. Создать бухгалтера")
print("2. Создать администратора")

choice = input("Выберите роль: ").strip()

if choice == "1":
    role_id = 1
    role_name = "Бухгалтер"
elif choice == "2":
    role_id = 2
    role_name = "Администратор"
else:
    print("Неверный выбор")
    exit()

login = input("Логин: ").strip()
password = input("Пароль: ").strip()
full_name = input("ФИО: ").strip()
address = input("Адрес: ").strip()

try:
    register(login, password, full_name, address, role_id)
    print(f"\n{role_name} успешно зарегистрирован!")
except Exception as e:
    print("Ошибка:", e)
