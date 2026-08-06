package aegis.llm.model_access

default allow = false
allow if { input.data_classification != "restricted" }
allow if { input.data_classification == "restricted"; input.model.provider == "local" }

