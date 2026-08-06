import re
from dataclasses import dataclass


@dataclass(frozen=True)
class GuardrailResult:
    allowed: bool
    reasons: tuple[str, ...] = ()


_INJECTION_PATTERNS = (
    re.compile(r"ignore (?:all |as |the )?(?:previous|anteriores?|instruções)", re.I),
    re.compile(r"(?:reveal|mostre|extraia).{0,30}(?:system prompt|instruções internas)", re.I),
    re.compile(r"(?:modo sem restrições|developer mode|jailbreak)", re.I),
)


def detect_prompt_injection(text: str) -> bool:
    return any(pattern.search(text) for pattern in _INJECTION_PATTERNS)


def inspect_input(prompt: str, documents: list[str] | None = None) -> GuardrailResult:
    reasons = []
    if detect_prompt_injection(prompt):
        reasons.append("direct_prompt_injection")
    if any(detect_prompt_injection(doc) for doc in documents or []):
        reasons.append("indirect_prompt_injection")
    return GuardrailResult(not reasons, tuple(reasons))