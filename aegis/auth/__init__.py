from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    tenant_id: str
    user_id: str
    role: str


def authenticate(tenant_id: str, user_id: str, role: str) -> Principal:
    if not tenant_id or not user_id:
        raise PermissionError("missing_identity")
    return Principal(tenant_id, user_id, role)

