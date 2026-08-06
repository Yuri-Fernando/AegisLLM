from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolContext:
    tenant_id: str
    user_id: str
    role: str = "support"


class SecureToolGateway:
    def __init__(self):
        self.records = {
            "tenant-a": {"customer": "Cliente A", "last_order": "Pedido A-100"},
            "tenant-b": {"customer": "Cliente B", "last_order": "Pedido B-200"},
        }
        self.created: list[dict[str, Any]] = []

    def execute(self, name: str, context: ToolContext, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        if name not in {"crm_read", "order_read", "rag_search", "create_lead", "schedule_meeting", "open_ticket"}:
            raise PermissionError(f"tool_denied:{name}")
        if context.tenant_id not in self.records:
            raise PermissionError("tenant_not_found")
        arguments = arguments or {}
        target_tenant = arguments.get("tenant_id", context.tenant_id)
        if target_tenant != context.tenant_id:
            raise PermissionError("cross_tenant_access_denied")
        data = self.records[context.tenant_id]
        if name == "crm_read":
            return {"customer": data["customer"]}
        if name == "order_read":
            return {"last_order": data["last_order"]}
        if name == "rag_search":
            return {"document": "Política comercial interna aprovada."}
        event = {"tool": name, "tenant_id": context.tenant_id, "status": "created"}
        self.created.append(event)
        return event