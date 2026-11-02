from dataclasses import dataclass

@dataclass
class User:
    id: int
    login: str
    password: str
    full_name: str
    address: str | None
    role_id: int
