# AegisLLM — Security Best Practices Report

Data da revisão: 2026-08-05  
Escopo: Python 3.11, FastAPI, gateway local, red team, CI/CD e container.

## Resumo executivo

A revisão encontrou uma API sem autenticação, request body arbitrário, ausência de controles de consumo e partes do pipeline de segurança que existiam como módulos mas não eram aplicadas pelo gateway. As falhas de maior impacto foram corrigidas. Não há finding crítico conhecido aberto no código local, mas o projeto continua sendo um laboratório: autenticação estática, controles em memória e adapters externos simulados não atendem requisitos de produção distribuída.

## Findings corrigidos

### SEC-001 — High — endpoint de geração sem autenticação

- Local anterior: `apps/api_gateway/main.py`, rota `/v1/secure-completions`.
- Impacto: qualquer cliente alcançando a API poderia consumir modelos e ferramentas.
- Correção: Bearer auth centralizada e comparação em tempo constante em `apps/api_gateway/dependencies.py:12-16`; identidade derivada da credencial.
- Status: corrigido.

### SEC-002 — High — identidade e autorização influenciáveis pelo payload

- Local anterior: `apps/api_gateway/main.py`, construção direta de `Request(**payload)`.
- Impacto: mass assignment de `tenant_id`, `role` e outros campos sensíveis.
- Correção: schema Pydantic com `extra="forbid"`, response model explícito e principal autenticado; rota em `apps/api_gateway/main.py:49`.
- Status: corrigido e coberto por teste.

### SEC-003 — High — tenant isolation incompleto no gateway de ferramentas

- Impacto: argumentos de ferramenta poderiam referenciar outro tenant.
- Correção: negação explícita em `aegis/tools.py:28` e teste cross-tenant.
- Status: corrigido.

### SEC-004 — High — módulos de output validation e RAG guardrails não integrados

- Impacto: saída com XSS/SQL e indirect prompt injection podiam atravessar o pipeline.
- Correção: guardrails antes da policy e validação de saída em `aegis/gateway.py:49`.
- Status: corrigido, com regressões adversariais.

### SEC-005 — Medium — ausência de proteção contra consumo excessivo

- Impacto: negação de carteira/CPU e abuso por usuário ou tenant.
- Correção: sliding-window rate limit e orçamento em memória em `aegis/gateway.py:21-29`.
- Status: corrigido para laboratório; controle distribuído permanece pendente.

### SEC-006 — Medium — auditoria com trace fixo e risco de dados brutos

- Impacto: colisão de eventos e potencial retenção indevida.
- Correção: UUID por request, hash SHA-256 do prompt em `aegis/gateway.py:64`, tipos de PII e metadados; prompts/respostas brutos não são persistidos.
- Status: corrigido.

### SEC-007 — Medium — baseline FastAPI incompleto

- Impacto: host-header abuse, docs expostas em produção, corpos grandes e respostas sem headers defensivos.
- Correção: Trusted Hosts em `apps/api_gateway/main.py:22`, docs desabilitadas em produção e middleware em `apps/api_gateway/main.py:29`.
- Status: corrigido no app; limites também devem existir no ingress/proxy.

### SEC-008 — Medium — container executava como root e tinha filesystem gravável

- Correção: usuário sem privilégio em `infrastructure/docker/Dockerfile:14`; Compose usa read-only, tmpfs, `no-new-privileges` e remove capabilities.
- Status: corrigido.

### SEC-009 — Medium — AppSec workflow não bloqueava findings e usava referência mutável

- Impacto: scans apenas informativos e risco de supply chain da action.
- Correção: Trivy falha em HIGH/CRITICAL e está preso ao SHA completo em `.github/workflows/appsec.yml:15`; Bandit e pip-audit adicionados.
- Status: corrigido para a action Trivy. Actions oficiais ainda usam tags major e podem ser pinadas por SHA como hardening adicional.

## Riscos residuais

### RES-001 — High em produção — autenticação estática de laboratório

O token único via ambiente não oferece rotação, expiração, audience/issuer, múltiplos tenants ou revogação. Antes de produção, usar OIDC/JWT rigorosamente validado e autorização por claims.

### RES-002 — High em produção — OPA não é decision point real

As policies Rego são artefatos de referência. A decisão executada ainda é Python. Integrar OPA/Conftest, garantir equivalência e fail-closed.

### RES-003 — Medium — rate limit e budget apenas em memória

Múltiplos workers/pods não compartilham estado. Migrar para Redis ou gateway gerenciado com chaves por tenant/usuário.

### RES-004 — Medium — adapters PyRIT/Garak/Promptfoo são contratos

Eles não executam scanners reais. Ao implementar, impor target allowlist, timeout, sandbox, limite de custo e confirmação de autorização.

### RES-005 — Medium — detecção heurística

Regex reduz ataques conhecidos, mas não substitui classificadores, segmentação de confiança, instruções estruturadas e avaliação contínua. Falsos negativos e positivos são esperados.

### RES-006 — Medium — serviços externos simulados

PostgreSQL/Supabase, Redis, LiteLLM, n8n, SOAP/SFTP e observabilidade real não foram testados contra serviços em execução.

## Verificação realizada

- compilação de todos os módulos Python;
- testes unitários, integração, segurança, adversariais, storage e API;
- benchmark funcional e security gates;
- execução top-to-bottom do notebook;
- Ruff, Bandit e auditoria de dependências quando disponíveis no ambiente instalado;
- validação de JSON, YAML/JSON simples e imports.

## Conclusão

O repositório agora demonstra de forma honesta uma arquitetura production-oriented e um laboratório reproduzível. Ele não deve ser descrito como solução production-ready até que os riscos residuais acima sejam tratados e validados em infraestrutura real.