import os
from typing import Any

import requests

from src.schemas import SensorReading


class HomeAssistantClient:
    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        timeout: int = 30,
    ) -> None:
        self.base_url = (
            base_url or os.getenv("HOME_ASSISTANT_URL", "http://192.168.8.251:8123")
        ).rstrip("/")
        self.token = token or os.getenv("HOME_ASSISTANT_TOKEN", "")
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        if not self.token:
            raise RuntimeError("HOME_ASSISTANT_TOKEN is not configured.")
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def get_states(self) -> list[SensorReading]:
        response = requests.get(
            f"{self.base_url}/api/states",
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()

        readings = []
        for item in response.json():
            readings.append(
                SensorReading(
                    entity_id=item["entity_id"],
                    state=str(item["state"]),
                    attributes=item.get("attributes", {}),
                    last_changed=item.get("last_changed"),
                )
            )
        return readings

    def get_state(self, entity_id: str) -> SensorReading:
        response = requests.get(
            f"{self.base_url}/api/states/{entity_id}",
            headers=self._headers(),
            timeout=self.timeout,
        )
        response.raise_for_status()
        item: dict[str, Any] = response.json()
        return SensorReading(
            entity_id=item["entity_id"],
            state=str(item["state"]),
            attributes=item.get("attributes", {}),
            last_changed=item.get("last_changed"),
        )

    def get_energy_state(self, entity_id: str = "sensor.home_energy_power") -> dict[str, Any]:
        reading = self.get_state(entity_id)
        return {
            "entity_id": reading.entity_id,
            "state": reading.state,
            "friendly_name": reading.attributes.get("friendly_name", reading.entity_id),
            "unit_of_measurement": reading.attributes.get("unit_of_measurement", ""),
            "last_changed": reading.last_changed,
        }
