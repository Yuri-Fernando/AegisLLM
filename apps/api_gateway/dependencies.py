import secrets

from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from aegis.auth import Principal
from aegis.config import Settings

bearer = HTTPBearer(auto_error=False)


def authenticate(credentials: HTTPAuthorizationCredentials | None, settings: Settings) -> Principal:
    if not settings.api_token:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="API authentication is not configured")
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    if not secrets.compare_digest(credentials.credentials, settings.api_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Principal(settings.api_tenant, settings.api_user, settings.api_role)