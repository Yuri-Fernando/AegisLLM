from .models import Request
from .router import Model


def generate(model: Model, request: Request) -> str:
    if "system prompt" in request.prompt.lower():
        return "Não posso revelar instruções internas. Posso ajudar com uma solicitação autorizada."
    if "saída maliciosa" in request.prompt.lower():
        return "<script>alert('xss')</script>"
    if request.requested_tool:
        return f"Modelo {model.name}: solicitação preparada para a ferramenta {request.requested_tool}."
    return f"Modelo {model.name}: resposta segura para a tarefa '{request.task}'."