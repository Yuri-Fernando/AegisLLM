def sanitize_document(document: str) -> tuple[str, bool]:
    markers = ("ignore previous", "system prompt", "exfiltrate", "reveal secret")
    poisoned = any(marker in document.lower() for marker in markers)
    return ("[DOCUMENT_REMOVED_AS_UNTRUSTED]" if poisoned else document, poisoned)

