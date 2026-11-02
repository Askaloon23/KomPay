from dataclasses import dataclass

@dataclass
class Accrual:
    id: int
    user_id: int
    service_id: int
    volume: float | None
    amount: float
    period: str
    accountant_id: int | None
    created_at: str | None = None
