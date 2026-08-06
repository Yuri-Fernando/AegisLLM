import json
import sqlite3
from pathlib import Path
from typing import Any

COUNT_QUERIES = {
    "model_registry": "SELECT COUNT(*) FROM model_registry",
    "evaluation_runs": "SELECT COUNT(*) FROM evaluation_runs",
    "redteam_findings": "SELECT COUNT(*) FROM redteam_findings",
    "audit_events": "SELECT COUNT(*) FROM audit_events",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS model_registry (
  id TEXT PRIMARY KEY, provider TEXT NOT NULL, model_name TEXT NOT NULL,
  supports_tools INTEGER NOT NULL, supports_json INTEGER NOT NULL,
  data_policy TEXT NOT NULL, cost REAL NOT NULL, enabled INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS evaluation_runs (
  id TEXT PRIMARY KEY, dataset_version TEXT NOT NULL, task TEXT NOT NULL,
  quality_score REAL NOT NULL, security_score REAL NOT NULL,
  success_rate REAL NOT NULL, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS redteam_findings (
  id TEXT PRIMARY KEY, run_id TEXT NOT NULL, attack_category TEXT NOT NULL,
  owasp_id TEXT NOT NULL, mitre_atlas_id TEXT NOT NULL, severity TEXT NOT NULL,
  attack_success INTEGER NOT NULL, evidence_hash TEXT NOT NULL, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit_events (
  trace_id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, model_id TEXT,
  tool_name TEXT, policy_decision INTEGER NOT NULL, risk_level TEXT NOT NULL,
  latency_ms REAL NOT NULL, prompt_hash TEXT NOT NULL, timestamp TEXT NOT NULL,
  metadata_json TEXT NOT NULL
);
"""


class LocalRepository:
    def __init__(self, path: str | Path = ":memory:"):
        self.connection = sqlite3.connect(str(path))
        self.connection.executescript(SCHEMA)

    def record_audit(self, event: dict[str, Any], tool_name: str | None = None) -> None:
        safe = {key: value for key, value in event.items() if key not in {"prompt", "response"}}
        self.connection.execute(
            "INSERT OR REPLACE INTO audit_events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (event["trace_id"], event["tenant_id"], event.get("model"), tool_name,
             int(event["policy_decision"]), event.get("risk_level", "unknown"),
             float(event.get("latency_ms", 0)), event["prompt_hash"], event["timestamp"],
             json.dumps(safe, ensure_ascii=False, sort_keys=True)),
        )
        self.connection.commit()

    def count(self, table: str) -> int:
        if table not in COUNT_QUERIES:
            raise ValueError("table not allowed")
        return int(self.connection.execute(COUNT_QUERIES[table]).fetchone()[0])