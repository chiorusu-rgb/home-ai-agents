from dataclasses import dataclass
from enum import Enum
from typing import Literal


class RoutedAgent(str, Enum):
    EMAIL = "email"
    ENERGY = "energy"
    HOMELAB_ARCHITECT = "homelab_architect"
    HOMELAB_ENGINEER = "homelab_engineer"


class RoutingMode(str, Enum):
    READ_ONLY = "read-only"
    PROPOSAL_ONLY = "proposal-only"
    APPROVED_EXECUTION = "approved-execution"


@dataclass
class RouteRequest:
    message: str
    context: dict


@dataclass
class RouteDecision:
    agent: RoutedAgent
    mode: RoutingMode
    requires_approval: bool
    rationale: str
    fallback: str | None = None


class ManagerAgent:
    def route(self, request: RouteRequest) -> RouteDecision:
        text = request.message.lower()

        if any(keyword in text for keyword in ["email", "inbox", "mail", "message"]):
            return RouteDecision(
                agent=RoutedAgent.EMAIL,
                mode=RoutingMode.READ_ONLY,
                requires_approval=False,
                rationale="Request is about email reading or summarization.",
            )

        if any(keyword in text for keyword in ["energy", "power", "temperature", "temp", "sensor", "home assistant"]):
            return RouteDecision(
                agent=RoutedAgent.ENERGY,
                mode=RoutingMode.READ_ONLY,
                requires_approval=False,
                rationale="Request is about energy, temperatures, or Home Assistant sensors.",
            )

        if any(keyword in text for keyword in ["architect", "design", "plan", "blueprint"]):
            return RouteDecision(
                agent=RoutedAgent.HOMELAB_ARCHITECT,
                mode=RoutingMode.PROPOSAL_ONLY,
                requires_approval=False,
                rationale="Request needs infrastructure design or planning.",
            )

        if any(keyword in text for keyword in ["engineer", "deploy", "create lxc", "proxmox", "apply", "execute"]):
            return RouteDecision(
                agent=RoutedAgent.HOMELAB_ENGINEER,
                mode=RoutingMode.PROPOSAL_ONLY,
                requires_approval=True,
                rationale="Request implies infrastructure implementation or execution.",
            )

        return RouteDecision(
            agent=RoutedAgent.HOMELAB_ARCHITECT,
            mode=RoutingMode.PROPOSAL_ONLY,
            requires_approval=False,
            rationale="Defaulted to architecture review for ambiguous infrastructure-related requests.",
            fallback="Ask for clarification if the target agent is unclear.",
        )
