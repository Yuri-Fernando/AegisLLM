package aegis.llm.tool_access

default allow = false
allow if { input.user.role == "support"; input.requested_tool == "order_read" }
allow if { input.user.role == "analyst"; input.requested_tool == "crm_read" }

