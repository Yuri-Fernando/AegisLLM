ORDERS = {"tenant-a": [{"id": "A-100", "status": "delivered"}], "tenant-b": [{"id": "B-200", "status": "open"}]}


def get_orders(tenant_id: str) -> list[dict]:
    return ORDERS.get(tenant_id, [])

