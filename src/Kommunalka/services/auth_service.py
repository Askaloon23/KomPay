from repositories import user_repository
from models.user import User

def authenticate(login: str, password: str) -> User | None:
    user = user_repository.get_by_login(login)
    if user and user.password == password:
        return user
    return None

def register(login: str, password: str, full_name: str, address: str, role_id: int = 3) -> int:
    if not login.strip() or not password.strip() or not full_name.strip():
        raise Exception("Логин, пароль и ФИО обязательны для заполнения")

    existing = user_repository.get_by_login(login)
    if existing:
        raise Exception("Пользователь с таким логином уже существует")

    return user_repository.create(login, password, full_name, address, role_id)
