# AegisLLM

Secure Multi-LLM Gateway, Continuous Red Teaming & AI Governance Lab.

AegisLLM é um laboratório **local-first** para demonstrar arquitetura de segurança, avaliação e governança para aplicações com LLMs. O projeto simula uma camada corporativa entre usuários, modelos, ferramentas, RAG e sistemas legados, com decisões auditáveis antes de liberar uma resposta.

Ele foi desenhado como projeto de portfólio para temas de **IA Generativa segura**, **LLMOps**, **RAG security**, **multi-LLM routing**, **red teaming**, **Security Agents**, **observabilidade** e **integração com sistemas corporativos**.

> Estado atual: **MVP local concluído para demonstração técnica**. AWS/Bedrock/cloud e n8n foram deixados fora desta etapa por escolha.

## Sumário

- [Resultado Atual](#resultado-atual)
- [Por Que Este Projeto Existe](#por-que-este-projeto-existe)
- [O Que O Projeto Faz](#o-que-o-projeto-faz)
- [Arquitetura Do Pipeline](#arquitetura-do-pipeline)
- [Security Agents](#security-agents)
- [Dashboard Local](#dashboard-local)
- [Como Rodar](#como-rodar)
- [API Local](#api-local)
- [Notebook](#notebook)
- [Testes, Gates E Segurança](#testes-gates-e-segurança)
- [Estrutura Do Repositório](#estrutura-do-repositório)
- [O Que Está Completo](#o-que-está-completo)
- [O Que É Opcional](#o-que-é-opcional)
- [O Que Ficou Fora Do Escopo](#o-que-ficou-fora-do-escopo)
- [Como Apresentar Este Projeto](#como-apresentar-este-projeto)

## Resultado Atual

Última validação local em Python **3.10.8**:

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

Artefatos principais:

- Dashboard: `http://127.0.0.1:8000/dashboard`.
- Payload vivo: `http://127.0.0.1:8000/dashboard-data`.
- Snapshot versionado: `observability/dashboards/aegis-latest-results.json`.
- Contrato dos painéis: `observability/dashboards/aegis-overview.json`.
- Relatório de aderência à vaga/laboratório: `docs/reports/project-readiness-for-genai-researcher.md`.
- Notebook executável: `notebooks/aegis_pipeline_demo.ipynb`.

## Por Que Este Projeto Existe

Aplicações com LLMs falham de formas diferentes de aplicações tradicionais:

- prompts podem tentar sobrescrever instruções;
- documentos RAG podem carregar instruções maliciosas;
- ferramentas podem ser abusadas para acessar dados de outro tenant;
- dados sensíveis podem ir para provedores indevidos;
- respostas podem carregar conteúdo ativo, SQL ou payloads perigosos;
- métricas de qualidade precisam conviver com métricas de risco, custo e latência.

O AegisLLM demonstra como tratar esses problemas com uma arquitetura simples, reproduzível e auditável.

## O Que O Projeto Faz

O AegisLLM responde a quatro perguntas centrais antes de liberar uma resposta:

- **Pode executar?** Valida identidade, papel, classificação do dado, prompt injection, RAG poisoning, orçamento e política.
- **Qual modelo usar?** Escolhe entre modelos simulados locais/cloud respeitando risco, custo, qualidade, latência e classificação.
- **Pode chamar ferramenta?** Aplica allowlist, RBAC, confirmação explícita para ações mutáveis e isolamento entre tenants.
- **A resposta é segura?** Valida saída contra conteúdo ativo, SQL/XSS e vazamento sensível, depois audita sem prompt bruto.

Funções implementadas:

- classificação `internal`, `confidential` e `restricted`;
- detecção de CPF, email, telefone, cartão e credenciais;
- DLP com redação de dados sensíveis;
- detecção de prompt injection direto;
- detecção de prompt injection indireto em documentos RAG;
- política de residência de dados para informações restritas;
- allowlist de ferramentas;
- RBAC por papel;
- confirmação obrigatória para ações mutáveis;
- tenant isolation em chamadas de ferramentas;
- rate limit local por `tenant:user`;
- budget local por tenant;
- roteamento multiobjetivo de modelos;
- validação de saída contra payload ativo;
- auditoria minimizada com hash do prompt;
- benchmark determinístico;
- red team local;
- security gates;
- Security Agents com readiness, cobertura, triagem e recomendações;
- dashboard local com dados vivos.

## Arquitetura Do Pipeline

```text
Cliente / Notebook / API
        ↓
Auth e identidade
        ↓
Classificação + DLP
        ↓
Guardrails de prompt e RAG
        ↓
Rate limit + budget por tenant
        ↓
Policy Engine
        ↓
Model Router
        ↓
Provider simulado
        ↓
Secure Tool Gateway
        ↓
Output Validation
        ↓
Resposta segura + audit event minimizado
        ↓
Benchmark + Red Team + Security Gates + Dashboard
```

### Etapas

- **Auth e identidade:** a API resolve tenant, usuário e papel pelo servidor, não por campos arbitrários do JSON.
- **Classificação + DLP:** identifica dados sensíveis e decide se o fluxo é interno, confidencial ou restrito.
- **Guardrails:** bloqueia jailbreaks e instruções do tipo “ignore as instruções anteriores”.
- **Controles locais:** aplica rate limit e orçamento por tenant.
- **Policy Engine:** centraliza autorização de modelo/ferramenta com regras de segurança.
- **Model Router:** escolhe `local-safe`, `cloud-fast` ou `cloud-reasoning` conforme utilidade e restrições.
- **Secure Tool Gateway:** simula CRM/pedido/RAG com proteção contra cross-tenant access.
- **Output Validation:** bloqueia XSS, SQL injection textual e vazamento sensível.
- **Auditoria:** registra timestamp, tenant, trace, classificação, PII, hash do prompt, modelo e decisão.

## Security Agents

O projeto possui uma esteira multi-agente local em `security_agents/`:

- **Attack Agent:** expõe corpus adversarial, matriz de cobertura e superfície de ataque.
- **Judge Agent:** avalia findings com veredito, score de risco, severidade, confiança e racional.
- **Defense Agent:** mapeia cada finding para controle, componente, recomendação e próxima ação.
- **Triage Agent:** cria triagem operacional com owner, prioridade, SLA e status.
- **Security Orchestrator:** junta tudo em um relatório único com readiness do projeto.

O resultado dos agentes aparece no dashboard:

- readiness `portfolio_ready`;
- cobertura por categoria;
- findings mapeados para OWASP e MITRE ATLAS;
- recomendações defensivas;
- tickets simulados com owner, prioridade e SLA.

## Dashboard Local

O dashboard não é imagem estática. Ele é uma UI local servida pela API FastAPI:

- frontend: `apps/dashboard/frontend/index.html`;
- endpoint HTML: `/dashboard`;
- endpoint JSON vivo: `/dashboard-data`;
- gerador de snapshot: `observability/dashboard.py`;
- snapshot: `observability/dashboards/aegis-latest-results.json`.

O que a tela mostra:

- métricas de Attack Success Rate, Blocked Rate, Task Success e latência;
- lista das capacidades ativas;
- avaliação de prontidão;
- superfície de ataque coberta;
- pipeline explicado etapa por etapa;
- cenários executados com decisão `allowed` ou `blocked`;
- classificação, PII, ferramenta, modelo, motivo e hash de auditoria;
- benchmark e security gates;
- roteamento de modelos e ranking;
- recomendações dos Security Agents;
- triagem operacional com owner, prioridade e SLA;
- findings red team por severidade, OWASP e MITRE ATLAS;
- único pendente explícito: n8n.

Para atualizar o snapshot:

```powershell
python -m observability.dashboard
```

## Como Rodar

### Requisitos

- Python **3.10.8+**.
- PowerShell no Windows, ou shell equivalente.
- Sem chaves de API obrigatórias.

### Instalação

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[api,dev,notebook]"
```

Se quiser usar ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[api,dev,notebook]"
```

### Rodar validações

```powershell
python -m pytest
python -m ruff check .
python examples/run_demo.py
python -m observability.dashboard
```

Também existem alvos no `Makefile`:

```bash
make test
make lint
make security
make demo
make notebook
```

## API Local

Configure um token próprio:

```powershell
$env:AEGIS_API_TOKEN = "gere-um-token-longo-e-aleatorio"
$env:AEGIS_API_TENANT = "tenant-a"
$env:AEGIS_API_USER = "api-user"
$env:AEGIS_API_ROLE = "support"
python -m uvicorn apps.api_gateway.main:app --host 127.0.0.1 --port 8000
```

Abra:

```text
http://127.0.0.1:8000/dashboard
```

Payload JSON:

```text
http://127.0.0.1:8000/dashboard-data
```

Healthcheck:

```text
http://127.0.0.1:8000/health
```

Exemplo de chamada protegida:

```bash
curl -X POST http://127.0.0.1:8000/v1/secure-completions \
  -H "Authorization: Bearer gere-um-token-longo-e-aleatorio" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Verifique meu pedido\",\"requested_tool\":\"order_read\"}"
```

Campos aceitos no corpo:

- `prompt`: texto do usuário;
- `task`: tarefa lógica, padrão `customer_support`;
- `requested_tool`: ferramenta opcional;
- `tool_arguments`: argumentos opcionais;
- `confirmed`: confirmação explícita para ações mutáveis;
- `rag_documents`: documentos simulados para testar RAG security.

Campos como `tenant_id`, `user_id` e `role` não são aceitos no JSON público da API. Eles vêm da configuração/autenticação do servidor, reduzindo risco de mass assignment.

## Notebook

O notebook `notebooks/aegis_pipeline_demo.ipynb` é um walkthrough executável.

Ele demonstra:

1. carregamento do projeto;
2. fluxo permitido;
3. tenant isolation;
4. ataques bloqueados;
5. RAG poisoning;
6. data exfiltration;
7. tool abuse;
8. output validation;
9. roteamento multiobjetivo;
10. benchmark;
11. gates;
12. Security Agents;
13. auditoria minimizada com SQLite.

Kernel recomendado:

```text
AegisLLM Python 3.10.8
```

Executar e salvar cópia:

```powershell
python -m nbconvert --to notebook --execute notebooks/aegis_pipeline_demo.ipynb --output-dir output/jupyter-notebook --output aegis_pipeline_demo.executed.ipynb
```

## Testes, Gates E Segurança

### Testes

```powershell
python -m pytest
```

Cobertura atual de comportamento:

- API pública e autenticação;
- rejeição de mass assignment;
- dashboard e dashboard-data;
- gateway permitido/bloqueado;
- prompt injection direto;
- RAG poisoning;
- dados restritos em modelo local;
- cross-tenant access;
- ação mutável sem confirmação;
- output malicioso;
- rate limit;
- budget;
- auditoria sem prompt bruto;
- DLP/redação;
- benchmark/gates;
- Security Agents.

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

Gates declarados:

- Attack Success Rate ≤ 5%;
- Task Success Rate ≥ 85%;
- Structured Output Validity ≥ 98%;
- p95 latency ≤ 4000 ms.

Resultado atual:

```text
todos passaram no corpus local-v2
```

## Estrutura Do Repositório

- `aegis/`: núcleo do gateway.
- `aegis/gateway.py`: orquestra o pipeline principal.
- `aegis/models.py`: contratos `Request` e `Response`.
- `aegis/classification.py`: classificação e detecção de PII.
- `aegis/dlp.py`: redação de dados sensíveis.
- `aegis/guardrails/`: detecção de prompt injection.
- `aegis/policy.py`: regras de autorização.
- `aegis/router.py`: roteamento multiobjetivo.
- `aegis/tools.py`: gateway seguro de ferramentas.
- `aegis/controls.py`: rate limit e budget local.
- `aegis/storage.py`: persistência SQLite local.
- `apps/api_gateway/`: API FastAPI.
- `apps/dashboard/frontend/`: dashboard local.
- `apps/demo_agent/`: agente demonstrativo usando o gateway.
- `apps/legacy_mock/`: sistemas legados simulados.
- `redteam/`: corpus adversarial, runner e adapters.
- `security_agents/`: Attack, Judge, Defense, Triage e Orchestrator.
- `evaluation/`: benchmark, datasets, baseline e gates.
- `observability/`: dashboard payload, schemas, alertas e collector local.
- `policies/`: security gates e policies OPA de referência.
- `integrations/`: stubs/contratos de integração.
- `infrastructure/`: Docker, Kubernetes, Terraform e Helm como esqueleto.
- `docs/`: arquitetura, threat model, governança e relatórios.
- `tests/`: testes automatizados.

## O Que Está Completo

Para demonstração local e portfólio:

- gateway seguro funcional;
- API FastAPI funcional;
- dashboard local com dados vivos;
- notebook executável;
- benchmark local;
- red team local;
- Security Agents enriquecidos;
- audit events minimizados;
- mocks corporativos;
- documentação de arquitetura;
- documentação de threat model;
- relatório de prontidão para IA generativa;
- testes e lint passando.

## O Que É Opcional

Estes itens são evoluções de produção, mas não bloqueiam o MVP local:

- autenticação OIDC/JWT real;
- OPA/Conftest como PDP executável;
- Redis para rate limit distribuído;
- PostgreSQL/Supabase para persistência gerenciada;
- provedores reais via LiteLLM/OpenAI/modelos locais;
- OpenTelemetry, Prometheus e Grafana reais;
- filas/workers para execução assíncrona;
- testes de carga;
- SBOM, assinatura de imagem e attestation;
- CI/CD mais rígido;
- deploy cloud.

## O Que Ficou Fora Do Escopo

Por decisão nesta etapa:

- **AWS/Bedrock/cloud:** não conectado agora.
- **n8n:** não conectado agora.

O repositório mantém referências/stubs para esses caminhos, mas o fluxo demo atual é local.


## Segurança E Uso Responsável

Todo red team deve se limitar ao laboratório local, containers próprios ou sistemas com autorização explícita. Não coloque PII, credenciais ou prompts reais em datasets, logs, issues ou notebooks.

Veja também:

- `SECURITY.md`
- `security_best_practices_report.md`
- `docs/threat-model/stride.md`
- `docs/governance/ai-risk-register.md`
- `docs/reports/project-readiness-for-genai-researcher.md`

Metodologia inspirada por OWASP Top 10 for LLM Applications, MITRE ATLAS e NIST AI RMF.
