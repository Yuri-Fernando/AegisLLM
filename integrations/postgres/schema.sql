CREATE TABLE model_registry (
  id UUID PRIMARY KEY, provider TEXT NOT NULL, model_name TEXT NOT NULL,
  deployment TEXT, supports_tools BOOLEAN NOT NULL, supports_json BOOLEAN NOT NULL,
  data_policy TEXT NOT NULL, cost_input NUMERIC, cost_output NUMERIC,
  context_window INTEGER, enabled BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE TABLE evaluation_runs (
  id UUID PRIMARY KEY, commit_sha TEXT, model_id UUID REFERENCES model_registry(id),
  dataset_version TEXT NOT NULL, task TEXT NOT NULL, quality_score NUMERIC,
  security_score NUMERIC, latency_p50 NUMERIC, latency_p95 NUMERIC,
  cost NUMERIC, success_rate NUMERIC, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE redteam_findings (
  id UUID PRIMARY KEY, run_id UUID NOT NULL, attack_category TEXT NOT NULL,
  owasp_id TEXT, mitre_atlas_id TEXT, severity TEXT NOT NULL,
  attack_success BOOLEAN NOT NULL, evidence_hash TEXT NOT NULL,
  recommendation TEXT, status TEXT NOT NULL
);
CREATE TABLE audit_events (
  trace_id UUID PRIMARY KEY, tenant_id TEXT NOT NULL, user_id_hash TEXT NOT NULL,
  model_id UUID, tool_name TEXT, policy_decision BOOLEAN NOT NULL,
  risk_level TEXT, tokens INTEGER, latency_ms NUMERIC, prompt_hash TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);