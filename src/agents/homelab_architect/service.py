from dataclasses import dataclass
from typing import Any


@dataclass
class ArchitectRequest:
    goal: str
    constraints: list[str]
    inventory: dict[str, Any]


@dataclass
class ArchitectResult:
    role: str
    mode: str
    proposal: str
    risks: list[str]
    rollback: list[str]


class HomelabArchitectAgent:
    role = "Homelab Architect"
    mode = "proposal-only"

    def run(self, request: ArchitectRequest) -> ArchitectResult:
        proposal = (
            f"Design a safe homelab plan for: {request.goal}. "
            f"Respect constraints: {', '.join(request.constraints) if request.constraints else 'none provided'}."
        )
        risks = [
            "Avoid testing against production VMIDs 100-500.",
            "Validate dependencies and rollback before execution.",
        ]
        rollback = [
            "Use sandbox-only testing first.",
            "Require Manager approval before any write action.",
        ]
        return ArchitectResult(
            role=self.role,
            mode=self.mode,
            proposal=proposal,
            risks=risks,
            rollback=rollback,
        )
