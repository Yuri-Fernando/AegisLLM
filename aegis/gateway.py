from datetime import datetime, timezone
from hashlib import sha256
from time import perf_counter

from .classification import classify
from .controls import BudgetExceeded, BudgetManager, RateLimitExceeded, SlidingWindowRateLimiter
from .guardrails import inspect_input
from .models import Request, Response
from .output_validation import validate_output
from .policy import evaluate
from .providers import generate
from .router import ModelRouter
from .tools import SecureToolGateway, ToolContext


class AegisGateway:
    def __init__(self, rate_limit: int = 30, budget_limit: float = 100.0):
        self.router = ModelRouter()
        self.tools = SecureToolGateway()
        self.audit_log: list[dict] = []
        self.rate_limiter = SlidingWindowRateLimiter(rate_limit)
        self.budgets = BudgetManager(budget_limit)

    def handle(self, request: Request) -> Response:
        started = perf_counter()
        classification, pii = classify(request.prompt)
        guardrails = inspect_input(request.prompt, request.rag_documents)
        try:
            self.rate_limiter.check(f"{request.tenant_id}:{request.user_id}")
            model = self.router.choose(request, classification)
            self.budgets.reserve(request.tenant_id, max(0.001, model.cost))
        except (RateLimitExceeded, BudgetExceeded, LookupError) as exc:
            return self._blocked(request, classification, pii, "controls", str(exc), started)
        decision = evaluate(request, classification, model.provider, guardrails)
        event = self._event(request, classification, pii, started, model.name, decision.allow, decision.reason)
        self.audit_log.append(event)
        if not decision.allow:
            return Response("blocked", "Requisição bloqueada pelo gateway.", model.name,
                            decision.risk_level, decision.reason, metadata=event)
        tool_result = None
        if request.requested_tool:
            try:
                context = ToolContext(request.tenant_id, request.user_id, request.role)
                tool_result = self.tools.execute(request.requested_tool, context, request.tool_arguments)
            except PermissionError as exc:
                event.update(policy_decision=False, reason=str(exc), tool_error=str(exc))
                return Response("blocked", "Chamada de ferramenta bloqueada.", model.name,
                                "high", str(exc), metadata=event)
        validation = validate_output(generate(model, request))
        event["latency_ms"] = round((perf_counter() - started) * 1000, 3)
        event["output_valid"] = validation.valid
        event["budget"] = self.budgets.snapshot(request.tenant_id)
        if not validation.valid:
            reason = ",".join(validation.reasons)
            event.update(policy_decision=False, reason=reason)
            return Response("blocked", "Saída bloqueada pelo gateway.", model.name,
                            "high", reason, metadata=event)
        return Response("allowed", validation.sanitized, model.name, decision.risk_level,
                        decision.reason, tool_result, event)

    def _event(self, request, classification, pii, started, model, allowed, reason) -> dict:
        return {"timestamp": datetime.now(timezone.utc).isoformat(), "tenant_id": request.tenant_id,
                "trace_id": request.trace_id, "classification": classification, "pii_types": pii,
                "prompt_hash": sha256(request.prompt.encode()).hexdigest(), "model": model,
                "policy_decision": allowed, "reason": reason,
                "latency_ms": round((perf_counter() - started) * 1000, 3)}

    def _blocked(self, request, classification, pii, stage, reason, started) -> Response:
        event = self._event(request, classification, pii, started, None, False, reason)
        event["stage"] = stage
        self.audit_log.append(event)
        return Response("blocked", "Requisição bloqueada pelo gateway.", risk_level="high",
                        policy_reason=reason, metadata=event)
