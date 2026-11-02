from services.auth_service import register

print("=== Создание сотрудников ===")

print("\n1. Создать бухгалтера")
print("2. Создать администратора")

choice = input("Выберите роль: ")

if choice == "1":
    role_id = 1
    role_name = "Бухгалтер"
elif choice == "2":
    role_id = 2
    role_name = "Администратор"
else:
    print("Неверный выбор")
    exit()

login = input("Логин: ")
password = input("Пароль: ")
full_name = input("ФИО: ")
address = input("Адрес: ")

try:
    register(
        login,
        password,
        full_name,
        address,
        role_id
    )
    print(f"\n{role_name} успешно зарегистрирован!")

except Exception as e:
    print("Ошибка:", e)