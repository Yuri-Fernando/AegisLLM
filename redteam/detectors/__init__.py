def blocked(response) -> bool:
    return getattr(response, "status", None) == "blocked"

