from aegis.telemetry import Trace


class LocalCollector:
    def collect(self, trace: Trace) -> dict:
        return {"trace_id": trace.trace_id, "span_count": len(trace.spans), "spans": trace.spans}

