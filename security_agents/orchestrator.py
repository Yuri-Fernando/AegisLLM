from dataclasses import dataclass

from redteam.runner import run_red_team, summarize
from security_agents.attack_agent import attack_surface_summary, coverage_matrix
from security_agents.defense_agent import recommend_control
from security_agents.judge_agent import judge
from security_agents.triage_agent import triage


@dataclass
class SecurityOrchestrator:
    """Executa Attack -> Judge -> Defense -> Triage contra o laboratório local."""

    def run(self, gateway=None) -> dict:
        findings = run_red_team(gateway)
        summary = summarize(findings)
        judgments = [judge(finding) for finding in findings]
        defense = [recommend_control(finding) for finding in findings]
        triage_report = triage(findings)
        failed_controls = [finding for finding in findings if finding["attack_success"]]
        return {
            "findings": findings,
            "summary": summary,
            "coverage": coverage_matrix(),
            "attack_surface": attack_surface_summary(),
            "judgments": judgments,
            "defense": defense,
            "triage": triage_report,
            "readiness": {
                "level": "portfolio_ready" if not failed_controls else "needs_security_fix",
                "score": round((1 - summary["attack_success_rate"]) * 100, 2),
                "blocked_by": [finding["name"] for finding in failed_controls],
                "open_items": ["n8n automation workflow"],
                "excluded_by_scope": ["AWS/cloud deployment"],
            },
        }
