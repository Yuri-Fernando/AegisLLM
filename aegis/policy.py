from dataclasses import dataclass

from .guardrails import GuardrailResult
from .models import Request


@dataclass(frozen=True)
class Decision:
    allow: bool
    reason: str
    risk_level: str = "low"


TOOL_ROLES = {
    "crm_read": {"analyst", "support", "admin"},
    "order_read": {"analyst", "support", "admin"},
    "rag_search": {"analyst", "support", "admin"},
    "create_lead": {"analyst", "admin"},
    "schedule_meeting": {"support", "analyst", "admin"},
    "open_ticket": {"support", "analyst", "admin"},
}
MUTATING_TOOLS = {"create_lead", "schedule_meeting", "open_ticket"}


def evaluate(request: Request, classification: str, model_provider: str = "local", guardrails: GuardrailResult | None = None) -> Decision:
    if request.role not in {"analyst", "support", "admin"}:
        return Decision(False, "papel sem permissão para o gateway", "high")
    if guardrails and not guardrails.allowed:
        return Decision(False, ",".join(guardrails.reasons), "high")
    if classification == "restricted" and (model_provider != "local" or "extern" in request.prompt.lower()):
        return Decision(False, "dados restritos só podem usar provedor local", "high")
    if request.requested_tool and request.requested_tool not in TOOL_ROLES:
        return Decision(False, f"ferramenta não autorizada: {request.requested_tool}", "high")
    if request.requested_tool and request.role not in TOOL_ROLES[request.requested_tool]:
        return Decision(False, "papel sem permissão para a ferramenta", "high")
    if request.requested_tool in MUTATING_TOOLS and not request.confirmed:
        return Decision(False, "ação mutável requer confirmação explícita", "medium")
    return Decision(True, "política permitiu a requisição", "medium" if classification != "internal" else "low")