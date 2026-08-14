from datetime import datetime, timezone
from typing import Any


class ReportingAgent:
    def build_report(self, sections: dict[str, Any]) -> dict[str, Any]:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "sections": sections,
            "mode": "read_only",
            "actions_executed": [],
        }
