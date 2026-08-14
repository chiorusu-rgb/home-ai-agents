from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class EmailMessage:
    message_id: str
    sender: str
    subject: str
    received_at: datetime
    body: str
    labels: list[str] = field(default_factory=list)


@dataclass
class EmailSummary:
    message_id: str
    category: str
    priority: str
    summary: str
    action_items: list[str] = field(default_factory=list)


@dataclass
class SensorReading:
    entity_id: str
    state: str
    attributes: dict[str, Any]
    last_changed: str | None = None


@dataclass
class EnergyReport:
    generated_at: datetime
    readings: list[SensorReading]
    observations: list[str]
    recommendations: list[str]
