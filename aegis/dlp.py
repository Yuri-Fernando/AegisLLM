import re


def redact(text: str) -> str:
    text = re.sub(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b", "[CPF_REDACTED]", text)
    text = re.sub(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b", "[EMAIL_REDACTED]", text)
    text = re.sub(r"\b(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b", "[PHONE_REDACTED]", text)
    text = re.sub(r"\b(?:\d[ -]*?){13,19}\b", "[CARD_REDACTED]", text)
    text = re.sub(r"(?i)\b(api[_ -]?key|password|senha|token|secret)\s*(=|:|é)\s*\S+", r"\1\2[CREDENTIAL_REDACTED]", text)
    return text


def contains_sensitive_output(text: str) -> bool:
    return redact(text) != text