import re
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

_IDENTIFIER = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$")


@dataclass
class Request:
    tenant_id: str
    user_id: str
    role: str
    prompt: str
    task: str = "customer_support"
    requested_tool: str | None = None
    data_classification: str | None = None
    trace_id: str = field(default_factory=lambda: str(uuid4()))
    tool_arguments: dict[str, Any] = field(default_factory=dict)
    confirmed: bool = False
    rag_documents: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        for name, value in (("tenant_id", self.tenant_id), ("user_id", self.user_id), ("role", self.role)):
            if not _IDENTIFIER.fullmatch(value):
                raise ValueError(f"{name} inválido")
        if not self.prompt.strip() or len(self.prompt) > 8_000:
            raise ValueError("prompt deve conter entre 1 e 8000 caracteres")
        if self.requested_tool and not _IDENTIFIER.fullmatch(self.requested_tool):
            raise ValueError("requested_tool inválido")
        if len(self.rag_documents) > 10 or any(len(doc) > 20_000 for doc in self.rag_documents):
            raise ValueError("limite de documentos RAG excedido")


@dataclass
class Response:
    status: str
    text: str
    model: str | None = None
    risk_level: str = "low"
    policy_reason: str = ""
    tool_result: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)