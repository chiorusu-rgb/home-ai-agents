from dataclasses import dataclass
from typing import Any


@dataclass
class EngineerRequest:
    plan: str
    approved: bool
    target: dict[str, Any]


@dataclass
class EngineerResult:
    role: str
    mode: str
    approved: bool
    action_summary: str
    blocked_reason: str | None


class HomelabEngineerAgent:
    role = "Homelab Engineer"

    def run(self, request: EngineerRequest) -> EngineerResult:
        mode = "approved-execution" if request.approved else "proposal-only"
        if not request.approved:
            return EngineerResult(
                role=self.role,
                mode=mode,
                approved=False,
                action_summary=f"Prepared execution proposal for target: {request.target}",
                blocked_reason="Manager approval required before any write action.",
            )
        return EngineerResult(
            role=self.role,
            mode=mode,
            approved=True,
            action_summary=f"Approved execution for target: {request.target}",
            blocked_reason=None,
        )
