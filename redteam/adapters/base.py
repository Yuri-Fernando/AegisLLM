from dataclasses import dataclass


@dataclass
class AdapterResult:
    tool: str
    available: bool
    findings: list[dict]
    error: str | None = None


class ExternalScannerAdapter:
    tool = "external-scanner"

    def run(self, target: str) -> AdapterResult:
        return AdapterResult(self.tool, False, [], "adapter disabled in local MVP")

