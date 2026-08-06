def list_drop_files(tenant_id: str) -> list[str]:
    return [f"{tenant_id}/orders.csv", f"{tenant_id}/contacts.csv"]

