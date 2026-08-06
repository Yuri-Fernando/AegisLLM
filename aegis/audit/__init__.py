import hashlib
import json


def evidence_hash(event: dict) -> str:
    payload = json.dumps(event, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()

