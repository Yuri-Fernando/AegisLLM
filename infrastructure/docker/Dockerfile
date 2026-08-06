FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system aegis && adduser --system --ingroup aegis aegis
COPY pyproject.toml README.md LICENSE ./
COPY aegis ./aegis
COPY apps ./apps
COPY evaluation ./evaluation
COPY redteam ./redteam
COPY security_agents ./security_agents
COPY integrations ./integrations
COPY observability ./observability
RUN python -m pip install --upgrade pip && python -m pip install ".[api]"
USER aegis
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["uvicorn", "apps.api_gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--no-proxy-headers"]