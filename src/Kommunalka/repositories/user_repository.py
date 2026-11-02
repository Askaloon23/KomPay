from database.database import get_connection
from models.user import User

def _map(row) -> User:
    return User(
        id=row["id"],
        login=row["login"],
        password=row["password"],
        full_name=row["full_name"],
        address=row["address"],
        role_id=row["role_id"]
    )

def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def create(login: str, password: str, full_name: str, address: str, role_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (login, password, full_name, address, role_id) VALUES (?, ?, ?, ?, ?)",
        (login, password, full_name, address, role_id)
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id

def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_residents() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE role_id = 3 ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]
