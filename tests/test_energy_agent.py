import unittest

from src.agents.energy.service import EnergyAgent
from src.schemas import SensorReading


class FakeLLM:
    def chat(self, system: str, user: str) -> str:
        return "Living room temperature is stable; power usage requires review."


class EnergyAgentTests(unittest.TestCase):
    def test_energy_agent_selects_relevant_sensors(self) -> None:
        readings = [
            SensorReading(
                entity_id="sensor.living_room_temperature",
                state="22.5",
                attributes={"unit_of_measurement": "°C"},
            ),
            SensorReading(
                entity_id="light.office",
                state="on",
                attributes={},
            ),
        ]

        result = EnergyAgent(FakeLLM()).analyze(readings)

        self.assertEqual(len(result.readings), 1)
        self.assertEqual(
            result.readings[0].entity_id,
            "sensor.living_room_temperature",
        )


if __name__ == "__main__":
    unittest.main()
