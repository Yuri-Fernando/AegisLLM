"""FastAPI adapter for the local-first AegisLLM gateway."""
from pathlib import Path

from aegis import AegisGateway, Request
from aegis.config import Settings
from observability.dashboard import build_dashboard_payload

DASHBOARD_HTML = Path(__file__).resolve().parents[1] / "dashboard" / "frontend" / "index.html"


def create_app(settings: Settings | None = None):
    from typing import Annotated

    from fastapi import APIRouter, Depends, FastAPI
    from fastapi import Request as HTTPRequest
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.security import HTTPAuthorizationCredentials
    from starlette.middleware.cors import CORSMiddleware
    from starlette.middleware.trustedhost import TrustedHostMiddleware

    from .dependencies import authenticate, bearer
    from .schemas import CompletionInput, CompletionOutput, HealthOutput

    settings = settings or Settings()
    gateway = AegisGateway()
    docs_url = None if settings.production else "/docs"
    openapi_url = None if settings.production else "/openapi.json"
    app = FastAPI(title="AegisLLM Gateway", version="0.2.0", docs_url=docs_url,
                  redoc_url=None, openapi_url=openapi_url, debug=False)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=list(settings.trusted_hosts))
    if settings.cors_origins:
        app.add_middleware(CORSMiddleware, allow_origins=list(settings.cors_origins),
                           allow_credentials=False, allow_methods=["POST"],
                           allow_headers=["Authorization", "Content-Type"])

    @app.middleware("http")
    async def security_baseline(request: HTTPRequest, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > settings.max_body_bytes:
            return JSONResponse({"detail": "Request body too large"}, status_code=413)
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/health", response_model=HealthOutput, include_in_schema=False)
    def health():
        return {"status": "ok", "service": "aegis-gateway"}

    @app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
    def dashboard():
        return DASHBOARD_HTML.read_text(encoding="utf-8")

    @app.get("/dashboard-data", include_in_schema=False)
    def dashboard_data():
        import platform

        return build_dashboard_payload(python_version=platform.python_version())

    router = APIRouter(prefix="/v1")

    def principal_dependency(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]):
        return authenticate(credentials, settings)

    @router.post("/secure-completions", response_model=CompletionOutput)
    def secure_completion(payload: CompletionInput,
                          principal: Annotated[object, Depends(principal_dependency)]):
        result = gateway.handle(Request(tenant_id=principal.tenant_id, user_id=principal.user_id,
            role=principal.role, prompt=payload.prompt, task=payload.task,
            requested_tool=payload.requested_tool, tool_arguments=payload.tool_arguments,
            confirmed=payload.confirmed, rag_documents=payload.rag_documents))
        return {"status": result.status, "text": result.text, "model": result.model,
                "risk_level": result.risk_level, "policy_reason": result.policy_reason,
                "tool_result": result.tool_result, "trace_id": result.metadata["trace_id"]}

    app.include_router(router)
    app.state.gateway = gateway
    return app


try:
    app = create_app()
except ImportError:
    app = None


if __name__ == "__main__":
    if app is None:
        raise SystemExit("Instale as dependências da API com: pip install -e .[api]")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
