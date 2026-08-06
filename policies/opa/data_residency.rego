package aegis.llm.data_residency

default allow = false
allow if { input.data_classification != "restricted" }
allow if { input.data_classification == "restricted"; input.model.provider == "local" }

