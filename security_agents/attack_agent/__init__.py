from redteam.runner import CASES, AttackCase


def generate_cases() -> list[AttackCase]:
    return list(CASES)


def coverage_matrix(cases: list[AttackCase] | None = None) -> list[dict]:
    rows = []
    for case in cases or CASES:
        rows.append({
            "name": case.name,
            "category": case.category,
            "owasp": case.owasp_id,
            "mitre_atlas": case.mitre_atlas_id,
            "severity": case.severity,
            "tests_tooling": bool(case.requested_tool),
            "tests_rag": bool(case.rag_documents),
            "tests_data_exfiltration": case.category == "data_exfiltration",
        })
    return rows


def attack_surface_summary(cases: list[AttackCase] | None = None) -> dict:
    rows = coverage_matrix(cases)
    categories = sorted({row["category"] for row in rows})
    return {
        "cases": len(rows),
        "categories": categories,
        "owasp": sorted({row["owasp"] for row in rows}),
        "mitre_atlas": sorted({row["mitre_atlas"] for row in rows}),
        "tool_cases": sum(row["tests_tooling"] for row in rows),
        "rag_cases": sum(row["tests_rag"] for row in rows),
        "data_exfiltration_cases": sum(row["tests_data_exfiltration"] for row in rows),
    }
