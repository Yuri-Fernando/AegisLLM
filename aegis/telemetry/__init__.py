from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class Trace:
    trace_id: str
    spans: list[dict] = field(default_factory=list)

    def add(self, name: str, **attributes):
        self.spans.append({"name": name, **attributes})


def timed(trace: Trace, name: str):
    start = perf_counter()
    def finish(**attributes):
        trace.add(name, duration_ms=round((perf_counter() - start) * 1000, 2), **attributes)
    return finish

