from collections import defaultdict, deque
from dataclasses import dataclass
from time import monotonic


class RateLimitExceeded(RuntimeError):
    pass


class BudgetExceeded(RuntimeError):
    pass


class SlidingWindowRateLimiter:
    def __init__(self, limit: int = 30, window_seconds: float = 60.0):
        self.limit = limit
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = monotonic()
        events = self._events[key]
        while events and events[0] <= now - self.window_seconds:
            events.popleft()
        if len(events) >= self.limit:
            raise RateLimitExceeded("rate_limit_exceeded")
        events.append(now)


@dataclass
class TenantBudget:
    max_units: float = 100.0
    used_units: float = 0.0


class BudgetManager:
    def __init__(self, default_limit: float = 100.0):
        self.default_limit = default_limit
        self._budgets: dict[str, TenantBudget] = {}

    def reserve(self, tenant_id: str, units: float) -> None:
        budget = self._budgets.setdefault(tenant_id, TenantBudget(self.default_limit))
        if units < 0 or budget.used_units + units > budget.max_units:
            raise BudgetExceeded("tenant_budget_exceeded")
        budget.used_units += units

    def snapshot(self, tenant_id: str) -> dict[str, float]:
        budget = self._budgets.setdefault(tenant_id, TenantBudget(self.default_limit))
        return {"used_units": round(budget.used_units, 4), "max_units": budget.max_units}