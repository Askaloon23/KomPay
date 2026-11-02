import hashlib, hmac
from repositories.repositories import users

# Хеширование пароля без сторонних библиотек.
def _hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register(login, password, full_name, address, role_id):
    if not login.strip() or not password or not full_name.strip():
        raise ValueError('Логин, пароль и ФИО обязательны.')
    if any(u.login.lower() == login.strip().lower() for u in users.get_all()):
        raise ValueError('Пользователь с таким логином уже существует.')
    return users.create(login=login.strip(), password=_hash(password), full_name=full_name.strip(),
                        address=address.strip() or None, user_role=int(role_id))

def authenticate(login, password):
    for user in users.get_all():
        if user.login.lower() == login.strip().lower():
            candidate = _hash(password)
            # Поддерживается вход в старые записи исходной БД с незахешированным паролем.
            if hmac.compare_digest(user.password, candidate) or hmac.compare_digest(user.password, password):
                if user.password == password:
                    users.update(user.user_id, password=candidate)
                return users.get_by_id(user.user_id)
    return None
