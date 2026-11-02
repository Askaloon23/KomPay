from dataclasses import dataclass

@dataclass
class Payment:
    id: int
    user_id: int
    accrual_id: int | None
    amount: float
    payment_method_id: int | None
    cashier_id: int | None
    paid_at: str | None = None
