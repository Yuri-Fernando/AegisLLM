import re

PII_PATTERNS = {
    "cpf": re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b"),
    "email": re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b", re.I),
    "phone": re.compile(r"\b(?:\+?55\s?)?\(?\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    "credential": re.compile(r"\b(?:api[_ -]?key|password|senha|token|secret)\s*(?:=|:|é)\s*\S+", re.I),
}


def detect_pii(text: str) -> list[str]:
    return [name for name, pattern in PII_PATTERNS.items() if pattern.search(text)]


def classify(text: str) -> tuple[str, list[str]]:
    pii = detect_pii(text)
    lowered = text.lower()
    if any(item in pii for item in ("credential", "credit_card")):
        return "restricted", pii
    if any(word in lowered for word in ("senha", "token", "secret", "cartão", "cartao", "confidencial")):
        return "restricted", pii
    if pii:
        return "confidential", pii
    return "internal", pii