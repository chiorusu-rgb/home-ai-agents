from datetime import datetime, timezone

from src.adapters.ollama_client import OllamaClient
from src.schemas import EnergyReport, SensorReading


class EnergyAgent:
    def __init__(self, llm: OllamaClient) -> None:
        self.llm = llm

    def analyze(self, readings: list[SensorReading]) -> EnergyReport:
        selected = [
            reading
            for reading in readings
            if reading.entity_id.startswith(("sensor.", "binary_sensor."))
            and any(
                term in reading.entity_id.lower()
                for term in ("temperature", "power", "energy", "battery", "humidity")
            )
        ]

        context = "\n".join(
            f"{item.entity_id}: {item.state} {item.attributes}"
            for item in selected
        )

        if not selected:
            return EnergyReport(
                generated_at=datetime.now(timezone.utc),
                readings=[],
                observations=["No matching energy or environmental sensors found."],
                recommendations=["Configure the Home Assistant entity allowlist."],
            )

        result = self.llm.chat(
            system=(
                "You are a read-only home energy and temperature analyst. "
                "Do not control devices or create automations."
            ),
            user=(
                "Analyze these Home Assistant readings. Identify unusual values, "
                "comfort issues, energy waste, and useful recommendations.\n\n"
                + context
            ),
        )

        return EnergyReport(
            generated_at=datetime.now(timezone.utc),
            readings=selected,
            observations=[result],
            recommendations=[
                "Review recommendations manually before creating any automation."
            ],
        )
