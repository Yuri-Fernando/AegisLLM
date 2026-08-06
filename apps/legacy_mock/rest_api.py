CUSTOMERS = {"tenant-a": {"id": "A-001", "name": "Cliente A"}, "tenant-b": {"id": "B-001", "name": "Cliente B"}}


def get_customer(tenant_id: str) -> dict:
    return CUSTOMERS[tenant_id]

