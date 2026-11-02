from database.database import get_connection
from models.service import Service

def _map(row) -> Service:
    return Service(
        id=row["id"],
        name=row["name"],
        unit=row["unit"],
        tariff=row["tariff"]
    )

def get_all() -> list[Service]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(service_id: int) -> Service | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services WHERE id = ?", (service_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None
