SEVERITY_PRIORITY = {"critical": 100, "high": 80, "medium": 50, "low": 20}
SEVERITY_SLA_HOURS = {"critical": 4, "high": 24, "medium": 72, "low": 168}
CATEGORY_OWNERS = {
    "prompt_injection": "AI Security",
    "rag_poisoning": "AI Security",
    "data_exfiltration": "Data Security",
    "tool_abuse": "Platform Security",
    "privilege_escalation": "Platform Security",
    "insecure_output": "AppSec",
    "jailbreak": "AI Security",
    "excessive_agency": "Agent Platform",
}


def triage(findings: list[dict]) -> list[dict]:
    tickets = []
    for finding in findings:
        severity = finding["severity"]
        open_status = bool(finding["attack_success"])
        tickets.append({
            "title": f"[{severity.upper()}] {finding['name']}",
            "category": finding["category"],
            "owasp": finding["owasp_id"],
            "mitre_atlas": finding["mitre_atlas_id"],
            "status": "open" if open_status else "mitigated",
            "owner": CATEGORY_OWNERS.get(finding["category"], "Security"),
            "priority": SEVERITY_PRIORITY.get(severity, 20) + (50 if open_status else 0),
            "sla_hours": SEVERITY_SLA_HOURS.get(severity, 168),
            "next_action": "corrigir e reexecutar red team" if open_status else "manter como teste de regressão",
        })
    return sorted(tickets, key=lambda ticket: ticket["priority"], reverse=True)
