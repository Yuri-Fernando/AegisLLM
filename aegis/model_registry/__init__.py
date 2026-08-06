from aegis.router import Model


class ModelRegistry:
    def __init__(self, models: list[Model] | None = None):
        self.models = {m.name: m for m in (models or [])}

    def register(self, model: Model) -> None:
        self.models[model.name] = model

    def enabled(self) -> list[Model]:
        return list(self.models.values())

