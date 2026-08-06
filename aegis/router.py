from dataclasses import dataclass

from .models import Request


@dataclass(frozen=True)
class Model:
    name: str
    provider: str
    quality: float
    cost: float
    latency_ms: float
    security_risk: float
    supports_tools: bool = True
    supports_json: bool = True
    failure_rate: float = 0.01
    allowed_classifications: tuple[str, ...] = ("public", "internal", "confidential")


class ModelRouter:
    def __init__(self, models: list[Model] | None = None):
        self.models = models or [
            Model("local-safe", "local", .84, .20, 850, .03,
                  allowed_classifications=("public", "internal", "confidential", "restricted")),
            Model("cloud-fast", "cloud", .88, .08, 420, .18, failure_rate=.03),
            Model("cloud-reasoning", "cloud", .96, .42, 1600, .10, failure_rate=.015),
        ]

    @staticmethod
    def utility(model: Model, request: Request) -> float:
        quality_weight = 2.0 if request.task in {"critical", "analysis"} else .6
        return (model.quality * quality_weight - model.cost * .25 - model.latency_ms / 10000
                - model.security_risk * .5 - model.failure_rate * .5)

    def choose(self, request: Request, classification: str) -> Model:
        candidates = [model for model in self.models if classification in model.allowed_classifications]
        if request.requested_tool:
            candidates = [model for model in candidates if model.supports_tools]
        if not candidates:
            raise LookupError("nenhum modelo atende às restrições obrigatórias")
        return max(candidates, key=lambda model: self.utility(model, request))

    def ranked(self, request: Request, classification: str) -> list[Model]:
        candidates = [model for model in self.models if classification in model.allowed_classifications]
        return sorted(candidates, key=lambda model: self.utility(model, request), reverse=True)

    def pareto_frontier(self) -> list[Model]:
        return [model for model in self.models if not any(
            other.quality >= model.quality and other.cost <= model.cost and
            other.security_risk <= model.security_risk and other != model
            for other in self.models
        )]