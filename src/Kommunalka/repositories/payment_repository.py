from database.database import get_connection
from models.payment import Payment

def _map(row) -> Payment:
    return Payment(
        id=row["id"],
        user_id=row["user_id"],
        accrual_id=row["accrual_id"],
        amount=row["amount"],
        payment_method_id=row["payment_method_id"],
        cashier_id=row["cashier_id"],
        paid_at=row["paid_at"]
    )

def create(user_id: int, amount: float, accrual_id: int | None = None,
           payment_method_id: int | None = None, cashier_id: int | None = None) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO payments (user_id, accrual_id, amount, payment_method_id, cashier_id)
           VALUES (?, ?, ?, ?, ?)""",
        (user_id, accrual_id, amount, payment_method_id, cashier_id)
    )
    conn.commit()
    payment_id = cur.lastrowid
    conn.close()
    return payment_id

def get_all() -> list[Payment]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_user(user_id: int) -> list[Payment]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(payment_id: int) -> Payment | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
