# Dashboard frontend

UI local do AegisLLM para auditoria, red-team findings, avaliações e health metrics.

Rode a API e abra:

```powershell
uvicorn apps.api_gateway.main:app --host 127.0.0.1 --port 8000
```

```text
http://127.0.0.1:8000/dashboard
```

O frontend consome o payload vivo de `/dashboard-data`.
