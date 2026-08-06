import re
from dataclasses import dataclass

from aegis.dlp import contains_sensitive_output, redact


@dataclass(frozen=True)
class OutputValidation:
    valid: bool
    sanitized: str
    reasons: tuple[str, ...]


def validate_output(text: str, max_chars: int = 4000) -> OutputValidation:
    reasons = []
    if len(text) > max_chars:
        reasons.append("output_too_large")
    if re.search(r"<script|javascript:|DROP\s+TABLE|UNION\s+SELECT", text, re.I):
        reasons.append("active_content_or_injection")
    if contains_sensitive_output(text):
        reasons.append("sensitive_output")
    return OutputValidation(not reasons, redact(text), tuple(reasons))