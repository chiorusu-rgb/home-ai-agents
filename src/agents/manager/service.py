from typing import Any


class ManagerAgent:
    READ_ONLY_ROLES = {
        "email": "email",
        "energy": "energy",
        "temperature": "energy",
        "report": "reporting",
        "summary": "reporting",
    }

    def route(self, request: str) -> dict[str, Any]:
        text = request.lower()
        for keyword, agent in self.READ_ONLY_ROLES.items():
            if keyword in text:
                return {
                    "agent": agent,
                    "mode": "read_only",
                    "requires_approval": False,
                    "request": request,
                }

        return {
            "agent": "manager",
            "mode": "proposal",
            "requires_approval": True,
            "request": request,
            "reason": "No safe read-only route matched.",
        }
