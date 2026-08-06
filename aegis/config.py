import os
from dataclasses import dataclass


def _csv(name: str, default: str) -> tuple[str, ...]:
    return tuple(value.strip() for value in os.getenv(name, default).split(",") if value.strip())


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("AEGIS_ENV", "local")
    api_token: str | None = os.getenv("AEGIS_API_TOKEN")
    api_tenant: str = os.getenv("AEGIS_API_TENANT", "tenant-a")
    api_user: str = os.getenv("AEGIS_API_USER", "api-user")
    api_role: str = os.getenv("AEGIS_API_ROLE", "support")
    trusted_hosts: tuple[str, ...] = _csv("AEGIS_TRUSTED_HOSTS", "localhost,127.0.0.1,testserver")
    cors_origins: tuple[str, ...] = _csv("AEGIS_CORS_ORIGINS", "")
    max_body_bytes: int = int(os.getenv("AEGIS_MAX_BODY_BYTES", "16384"))

    @property
    def production(self) -> bool:
        return self.environment.lower() == "production"