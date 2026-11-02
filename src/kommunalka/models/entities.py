from dataclasses import dataclass

@dataclass
class UserRole:
    user_role_id: int; name: str
@dataclass
class Service:
    service_id: int; name: str; unit: str; tariff: float
@dataclass
class PaymentMethod:
    method_id: int; name: str
@dataclass
class User:
    user_id: int; login: str; password: str; full_name: str; address: str | None; user_role: int
@dataclass
class Accrual:
    accrual_id: int; resident_id: int; service_id: int; accountant_id: int
    period: str; volume: float; amount: float
@dataclass
class Payment:
    payment_id: int; accrual_id: int; method_id: int; amount: float; payment_date: str; status: str
@dataclass
class Receipt:
    receipt_id: int; payment_id: int; number: str; issue_date: str
