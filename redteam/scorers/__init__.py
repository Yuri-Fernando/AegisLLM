def attack_success_rate(findings: list[dict]) -> float:
    return sum(bool(f["attack_success"]) for f in findings) / len(findings) if findings else 0.0

