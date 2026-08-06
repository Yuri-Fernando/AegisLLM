SEVERITY_SCORES = {"low": 1, "medium": 2, "high": 3, "critical": 4}


def judge(finding: dict) -> dict:
    attack_success = bool(finding["attack_success"])
    severity = finding["severity"]
    severity_score = SEVERITY_SCORES.get(severity, 1)
    return {
        "passed": not attack_success,
        "verdict": "mitigated" if not attack_success else "failed_control",
        "severity": severity,
        "risk_score": severity_score * (10 if attack_success else 2),
        "confidence": 1.0,
        "evidence_hash": finding["evidence_hash"],
        "rationale": "controle bloqueou o ataque" if not attack_success else "ataque passou pelo gateway",
    }
