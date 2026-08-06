from aegis import AegisGateway, Request


class CorporateSupportAgent:
    """Agente demonstrativo; toda ferramenta passa pelo gateway seguro."""

    TOOL_KEYWORDS = {
        "order_read": ("pedido", "compra"),
        "crm_read": ("cliente", "cadastro"),
        "rag_search": ("documento", "política"),
        "open_ticket": ("chamado", "ticket"),
        "schedule_meeting": ("reunião", "agendar"),
        "create_lead": ("lead", "prospect"),
    }

    def __init__(self, gateway: AegisGateway | None = None):
        self.gateway = gateway or AegisGateway()

    def answer(self, tenant_id: str, user_id: str, question: str,
               role: str = "support", confirmed: bool = False) -> dict:
        lowered = question.lower()
        tool = next((name for name, words in self.TOOL_KEYWORDS.items()
                     if any(word in lowered for word in words)), None)
        result = self.gateway.handle(Request(tenant_id, user_id, role, question,
                                             requested_tool=tool, confirmed=confirmed))
        return {"status": result.status, "answer": result.text, "model": result.model,
                "reason": result.policy_reason, "tool": result.tool_result,
                "trace_id": result.metadata["trace_id"]}