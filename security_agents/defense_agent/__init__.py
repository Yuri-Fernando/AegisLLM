CONTROL_DETAILS = {
    "LLM01": {
        "control": "Prompt/RAG Injection Defense",
        "recommendation": "input/RAG prompt-injection detector + regression test",
        "component": "aegis.guardrails",
    },
    "LLM05": {
        "control": "Output Validation",
        "recommendation": "output validation + contextual encoding at consumer",
        "component": "aegis.output_validation",
    },
    "LLM06": {
        "control": "Sensitive Data Protection",
        "recommendation": "classification, DLP and provider data-residency policy",
        "component": "aegis.classification + aegis.policy",
    },
    "LLM08": {
        "control": "Tool Governance",
        "recommendation": "tool allowlist, least privilege, tenant isolation and confirmation",
        "component": "aegis.policy + aegis.tools",
    },
}


def recommend(finding: dict) -> str:
    return recommend_control(finding)["recommendation"]


def recommend_control(finding: dict) -> dict:
    detail = CONTROL_DETAILS.get(finding["owasp_id"], {
        "control": "Manual Review",
        "recommendation": "manual security review",
        "component": "security_agents",
    })
    return {
        "finding": finding["name"],
        "owasp": finding["owasp_id"],
        "control": detail["control"],
        "component": detail["component"],
        "recommendation": detail["recommendation"],
        "implemented": not finding["attack_success"],
        "next_action": "manter regressão automatizada" if not finding["attack_success"] else "priorizar correção antes de release",
    }
