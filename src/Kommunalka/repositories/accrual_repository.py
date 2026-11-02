from database.database import get_connection
from models.accrual import Accrual

def _map(row) -> Accrual:
    return Accrual(
        id=row["id"],
        user_id=row["user_id"],
        service_id=row["service_id"],
        volume=row["volume"],
        amount=row["amount"],
        period=row["period"],
        accountant_id=row["accountant_id"],
        created_at=row["created_at"]
    )

def create(user_id: int, service_id: int, amount: float, period: str,
           accountant_id: int | None = None, volume: float | None = None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO accruals (user_id, service_id, volume, amount, period, accountant_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, service_id, volume, amount, period, accountant_id)
    )
    conn.commit()
    accrual_id = cur.lastrowid
    conn.close()
    return accrual_id

def get_all() -> list[Accrual]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accruals ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_user(user_id: int) -> list[Accrual]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accruals WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(accrual_id: int) -> Accrual | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM accruals WHERE id = ?", (accrual_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
