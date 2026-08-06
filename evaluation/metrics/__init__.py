def success_rate(results: list[dict]) -> float:
    return sum(r.get("success", False) for r in results) / len(results) if results else 0.0


def structured_validity(results: list[dict]) -> float:
    return sum(r.get("schema_valid", False) for r in results) / len(results) if results else 0.0

