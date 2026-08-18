# AegisLLM

### Secure Multi-LLM Gateway · Continuous Red Teaming · AI Governance Lab

## Status

🟢 **Concluído — MVP local para demonstração técnica**

O AegisLLM é um laboratório **local-first** desenvolvido para demonstrar uma arquitetura de segurança, avaliação e governança para aplicações com LLMs. O sistema simula uma camada intermediária entre usuários, modelos, ferramentas, RAG e sistemas legados, aplicando decisões de segurança antes da liberação de respostas.

O projeto explora **IA Generativa segura, LLMOps, RAG Security, Multi-LLM Routing, Red Teaming, Security Agents, observabilidade e integração com sistemas corporativos**.

---

## Sobre o projeto

Aplicações baseadas em LLM possuem riscos diferentes dos sistemas tradicionais, incluindo **prompt injection, RAG poisoning, uso indevido de ferramentas, vazamento de dados sensíveis e respostas contendo conteúdo potencialmente perigoso**.

O AegisLLM foi estruturado para demonstrar como esses riscos podem ser tratados por meio de uma arquitetura reproduzível e auditável, combinando controles de segurança, roteamento de modelos, validação de saída, avaliação automatizada e governança.

---

## Objetivos

O projeto organiza a tomada de decisão em quatro perguntas principais:

* **Pode executar?** Validação de identidade, papel, classificação dos dados, prompt injection, RAG poisoning, orçamento e políticas.
* **Qual modelo utilizar?** Roteamento entre diferentes perfis de modelo considerando risco, custo, qualidade e latência.
* **Pode utilizar uma ferramenta?** Allowlist, RBAC, confirmação explícita para operações mutáveis e isolamento entre tenants.
* **A resposta é segura?** Validação contra conteúdo ativo, SQL/XSS e vazamento de informações sensíveis, seguida de auditoria minimizada.

---

## Funcionalidades

### Segurança e Governança

* Classificação de dados em `internal`, `confidential` e `restricted`;
* Detecção de CPF, e-mail, telefone, cartão e credenciais;
* DLP com redação de informações sensíveis;
* Detecção de prompt injection direto;
* Detecção de prompt injection indireto em documentos RAG;
* Política de residência de dados para informações restritas;
* Allowlist de ferramentas;
* RBAC por papel;
* Confirmação obrigatória para ações mutáveis;
* Isolamento entre tenants;
* Rate limit local por `tenant:user`;
* Budget local por tenant;
* Roteamento multiobjetivo de modelos;
* Validação de saída contra payloads ativos;
* Auditoria minimizada com hash do prompt.

### Avaliação e Red Teaming

* Benchmark determinístico;
* Corpus adversarial local;
* Red Team automatizado;
* Security Gates;
* Security Agents;
* Avaliação de cobertura;
* Triagem e recomendações;
* Findings associados a OWASP e MITRE ATLAS.

### Observabilidade

* Dashboard local com dados vivos;
* Métricas de Attack Success Rate, Blocked Rate e Task Success;
* Avaliação de readiness;
* Cobertura da superfície de ataque;
* Pipeline visual de segurança;
* Rastreamento de modelo, ferramenta, classificação, decisão e hash de auditoria;
* Ranking de roteamento de modelos;
* Recomendações dos Security Agents;
* Triagem operacional com owner, prioridade e SLA.

---

## Arquitetura

```text
Cliente / Notebook / API
        ↓
Auth e Identidade
        ↓
Classificação + DLP
        ↓
Guardrails de Prompt e RAG
        ↓
Rate Limit + Budget por Tenant
        ↓
Policy Engine
        ↓
Model Router
        ↓
Provider Simulado
        ↓
Secure Tool Gateway
        ↓
Output Validation
        ↓
Resposta Segura + Audit Event Minimizado
        ↓
Benchmark + Red Team + Security Gates + Dashboard
```

### Etapas principais

* **Auth e Identidade:** resolve tenant, usuário e papel por configuração/autenticação do servidor.
* **Classificação + DLP:** identifica dados sensíveis e define a classificação do fluxo.
* **Guardrails:** bloqueia jailbreaks e instruções maliciosas.
* **Controles locais:** aplica rate limit e orçamento por tenant.
* **Policy Engine:** centraliza autorização de modelos e ferramentas.
* **Model Router:** seleciona `local-safe`, `cloud-fast` ou `cloud-reasoning` conforme as restrições.
* **Secure Tool Gateway:** simula CRM, pedidos e RAG com proteção contra acesso entre tenants.
* **Output Validation:** bloqueia XSS, SQL injection textual e vazamento sensível.
* **Auditoria:** registra timestamp, tenant, trace, classificação, PII, hash do prompt, modelo e decisão.

---

## Security Agents

O projeto possui uma esteira multiagente especializada em segurança:

| Agent                     | Responsabilidade                                                |
| ------------------------- | --------------------------------------------------------------- |
| **Attack Agent**          | Corpus adversarial, cobertura e superfície de ataque            |
| **Judge Agent**           | Avaliação dos findings, risco, severidade, confiança e racional |
| **Defense Agent**         | Mapeamento de findings para controles e recomendações           |
| **Triage Agent**          | Owner, prioridade, SLA e status                                 |
| **Security Orchestrator** | Consolidação dos resultados e readiness                         |

Os resultados são apresentados no dashboard, incluindo cobertura, findings, recomendações defensivas e tickets simulados.

---

## Resultado Atual

Última validação local utilizando **Python 3.10.8**:

```text
pytest: 23 passed
benchmark dataset: local-v2

task success rate: 100%
structured output validity: 100%

attack success rate: 0%
red team cases: 8
blocked rate: 100%

security gates: passed
readiness: portfolio_ready
```

Esses resultados correspondem ao corpus local utilizado na validação do projeto.

### Artefatos principais

* Dashboard: `http://127.0.0.1:8000/dashboard`
* Payload vivo: `http://127.0.0.1:8000/dashboard-data`
* Snapshot versionado: `observability/dashboards/aegis-latest-results.json`
* Contrato dos painéis: `observability/dashboards/aegis-overview.json`
* Relatório de readiness: `docs/reports/project-readiness-for-genai-researcher.md`
* Notebook executável: `notebooks/aegis_pipeline_demo.ipynb`

---

## Dashboard Local

O dashboard é uma interface local servida pela API FastAPI, e não uma imagem estática.

### Componentes

* Frontend: `apps/dashboard/frontend/index.html`
* Interface: `/dashboard`
* Dados vivos: `/dashboard-data`
* Gerador de snapshot: `observability/dashboard.py`
* Snapshot: `observability/dashboards/aegis-latest-results.json`

### Métricas e informações

* Attack Success Rate;
* Blocked Rate;
* Task Success;
* Latência;
* Capacidades ativas;
* Readiness;
* Cobertura da superfície de ataque;
* Cenários executados;
* Classificação e PII;
* Modelo e ferramenta;
* Motivo da decisão;
* Hash de auditoria;
* Benchmark e Security Gates;
* Roteamento de modelos;
* Recomendações dos Security Agents;
* Findings por severidade;
* OWASP e MITRE ATLAS;
* Triagem operacional.

Para atualizar o snapshot:

```powershell
python -m observability.dashboard
```

---

## Tecnologias

### AI & LLM Security

* Python
* LLMs
* Multi-LLM Routing
* RAG Security
* Prompt Injection Detection
* RAG Poisoning Detection
* Security Agents
* Red Teaming
* AI Governance

### Backend & API

* FastAPI
* REST API
* SQLite
* Python

### Evaluation & Observability

* Benchmarking
* Security Gates
* Red Team Evaluation
* Langfuse-compatible observability concepts
* Structured Logging
* Telemetry
* Dashboard local

### Security Frameworks

* OWASP Top 10 for LLM Applications
* MITRE ATLAS
* NIST AI RMF

### Infrastructure & Engineering

* Docker
* Kubernetes
* Terraform
* Helm
* GitHub Actions
* CI/CD
* OPA / Policy-as-Code concepts

---

## Como executar

### Requisitos

* Python **3.10.8+**
* PowerShell no Windows ou shell equivalente
* Não são necessárias chaves de API para executar o MVP local.

### Instalação

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[api,dev,notebook]"
```

### Ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install -e ".[api,dev,notebook]"
```

### Validação

```powershell
python -m pytest
python -m ruff check .
python examples/run_demo.py
python -m observability.dashboard
```

Também existem comandos no `Makefile`:

```bash
make test
make lint
make security
make demo
make notebook
```

---

## API Local

Configure um token próprio:

```powershell
$env:AEGIS_API_TOKEN = "gere-um-token-longo-e-aleatorio"
$env:AEGIS_API_TENANT = "tenant-a"
$env:AEGIS_API_USER = "api-user"
$env:AEGIS_API_ROLE = "support"

python -m uvicorn apps.api_gateway.main:app --host 127.0.0.1 --port 8000
```

### Endpoints

Dashboard:

```text
http://127.0.0.1:8000/dashboard
```

Dashboard Data:

```text
http://127.0.0.1:8000/dashboard-data
```

Healthcheck:

```text
http://127.0.0.1:8000/health
```

---

## Exemplo de chamada

```bash
curl -X POST http://127.0.0.1:8000/v1/secure-completions \
  -H "Authorization: Bearer gere-um-token-longo-e-aleatorio" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Verifique meu pedido\",\"requested_tool\":\"order_read\"}"
```

### Campos aceitos

* `prompt`
* `task`
* `requested_tool`
* `tool_arguments`
* `confirmed`
* `rag_documents`

Campos como `tenant_id`, `user_id` e `role` não são aceitos diretamente no JSON público da API, sendo obtidos pela configuração/autenticação do servidor.

---

## Notebook

O notebook:

```text
notebooks/aegis_pipeline_demo.ipynb
```

é um walkthrough executável que demonstra:

1. carregamento do projeto;
2. fluxo permitido;
3. isolamento entre tenants;
4. ataques bloqueados;
5. RAG poisoning;
6. data exfiltration;
7. tool abuse;
8. output validation;
9. roteamento multiobjetivo;
10. benchmark;
11. security gates;
12. Security Agents;
13. auditoria minimizada com SQLite.

---

## Testes, Gates e Segurança

### Testes

```powershell
python -m pytest
```

A suíte cobre:

* API pública e autenticação;
* rejeição de mass assignment;
* dashboard e dashboard-data;
* gateway permitido/bloqueado;
* prompt injection;
* RAG poisoning;
* dados restritos;
* cross-tenant access;
* ações mutáveis sem confirmação;
* output malicioso;
* rate limit;
* budget;
* auditoria sem prompt bruto;
* DLP;
* benchmark;
* security gates;
* Security Agents.

### Lint

```powershell
python -m ruff check .
```

### Security Checks

```powershell
bandit -q -r aegis apps redteam security_agents evaluation
pip-audit
```

### Gates

```text
Attack Success Rate        ≤ 5%
Task Success Rate          ≥ 85%
Structured Output Validity ≥ 98%
p95 latency                ≤ 4000 ms
```

Resultado atual:

```text
Todos os gates passaram no corpus local-v2.
```

---

## Estrutura do Repositório

```text
AegisLLM/
├── aegis/
│   ├── gateway.py
│   ├── models.py
│   ├── classification.py
│   ├── dlp.py
│   ├── guardrails/
│   ├── policy.py
│   ├── router.py
│   ├── tools.py
│   ├── controls.py
│   └── storage.py
│
├── apps/
│   ├── api_gateway/
│   ├── dashboard/
│   ├── demo_agent/
│   └── legacy_mock/
│
├── redteam/
├── security_agents/
├── evaluation/
├── observability/
├── policies/
├── integrations/
├── infrastructure/
├── docs/
├── notebooks/
└── tests/
```

### Principais responsabilidades

* `aegis/` — núcleo do gateway e controles de segurança;
* `apps/api_gateway/` — API FastAPI;
* `apps/dashboard/` — interface local;
* `redteam/` — corpus e execução dos ataques;
* `security_agents/` — Attack, Judge, Defense, Triage e Orchestrator;
* `evaluation/` — benchmark, datasets e gates;
* `observability/` — dashboard, schemas e métricas;
* `policies/` — security gates e políticas;
* `integrations/` — contratos e stubs;
* `infrastructure/` — Docker, Kubernetes, Terraform e Helm;
* `docs/` — arquitetura, threat model e governança;
* `tests/` — testes automatizados.

---

## O que este projeto demonstra

* Arquitetura segura para aplicações com LLMs;
* Multi-LLM routing;
* RAG security;
* Prompt injection detection;
* DLP e classificação de dados;
* RBAC e tenant isolation;
* Tool security;
* Output validation;
* AI Governance;
* Red Teaming;
* Security Agents;
* Benchmarking e Security Gates;
* Observabilidade;
* API design com FastAPI;
* Automação de testes;
* CI/CD e AppSec;
* Threat modeling;
* Auditoria minimizada;
* Engenharia de software aplicada a GenAI.

---

## O que está completo

O MVP atual possui:

* Gateway seguro funcional;
* API FastAPI funcional;
* Dashboard local com dados vivos;
* Notebook executável;
* Benchmark local;
* Red Team local;
* Security Agents;
* Audit events minimizados;
* Mocks corporativos;
* Documentação de arquitetura;
* Threat Model;
* Relatório de readiness;
* Testes e lint.

---

## Melhorias e Evoluções Futuras

Os seguintes componentes foram planejados como evoluções da arquitetura:

* OIDC/JWT real;
* OPA/Conftest como PDP executável;
* Redis para rate limiting distribuído;
* PostgreSQL/Supabase;
* Provedores reais via LiteLLM, OpenAI ou modelos locais;
* OpenTelemetry, Prometheus e Grafana;
* Filas e workers assíncronos;
* Testes de carga;
* SBOM, assinatura de imagem e attestation;
* CI/CD mais rigoroso;
* Deploy em cloud.

### Fora do escopo desta versão

Por decisão arquitetural, esta versão não conecta:

* **AWS / Bedrock / cloud**
* **n8n**

O repositório mantém referências e stubs para esses caminhos, mas o fluxo demonstrativo atual é completamente local.

---

## Segurança e Uso Responsável

Os testes de Red Team devem ser executados exclusivamente em ambiente local, containers próprios ou sistemas para os quais exista autorização explícita.

Não utilize PII, credenciais, prompts reais ou informações sensíveis em datasets, logs, notebooks, issues ou exemplos.

Documentação complementar:

* `SECURITY.md`
* `security_best_practices_report.md`
* `docs/threat-model/stride.md`
* `docs/governance/ai-risk-register.md`
* `docs/reports/project-readiness-for-genai-researcher.md`

A metodologia do projeto utiliza referências de **OWASP Top 10 for LLM Applications, MITRE ATLAS e NIST AI RMF**.

---

## Licença

Consulte o arquivo `LICENSE` deste repositório para informações sobre uso e distribuição.

---

## Autor

**Yuri Fernando Dubbern**

AI/ML Engineer · Generative AI · Data Engineering · Intelligent Automation

[LinkedIn](https://www.linkedin.com/in/yuridubbern) · [GitHub](https://github.com/Yuri-Fernando) · [Lattes](http://lattes.cnpq.br/7151392692642166) · [Linktree](https://linktr.ee/yuri.f.dubbern)
