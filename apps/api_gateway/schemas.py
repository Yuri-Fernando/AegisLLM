from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Document = Annotated[str, Field(max_length=20_000)]


class CompletionInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = Field(min_length=1, max_length=8000)
    task: str = Field(default="customer_support", max_length=64, pattern=r"^[a-zA-Z0-9._-]+$")
    requested_tool: str | None = Field(default=None, max_length=64, pattern=r"^[a-zA-Z0-9._-]+$")
    tool_arguments: dict[str, Any] = Field(default_factory=dict)
    confirmed: bool = False
    rag_documents: list[Document] = Field(default_factory=list, max_length=10)


class CompletionOutput(BaseModel):
    status: Literal["allowed", "blocked"]
    text: str
    model: str | None
    risk_level: str
    policy_reason: str
    tool_result: Any = None
    trace_id: str


class HealthOutput(BaseModel):
    status: Literal["ok"]
    service: str