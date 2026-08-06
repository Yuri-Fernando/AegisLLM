def get_customer_soap(tenant_id: str) -> str:
    return f"<Customer><Tenant>{tenant_id}</Tenant><Status>active</Status></Customer>"

