package aegis.llm.tenant_isolation

default allow = false
allow if { input.resource.tenant_id == input.user.tenant_id }

