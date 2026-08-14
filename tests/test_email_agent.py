import unittest
from datetime import datetime, timezone

from src.agents.email.service import EmailAgent
from src.schemas import EmailMessage


class FakeLLM:
    def chat(self, system: str, user: str) -> str:
        return (
            "CATEGORY: homelab\n"
            "PRIORITY: high\n"
            "SUMMARY: Wazuh reported a new security event.\n"
            "ACTIONS: Review the alert in Wazuh"
        )


class EmailAgentTests(unittest.TestCase):
    def test_email_is_summarized_without_side_effects(self) -> None:
        message = EmailMessage(
            message_id="test-1",
            sender="wazuh@example.local",
            subject="Security alert",
            received_at=datetime.now(timezone.utc),
            body="A test alert occurred.",
        )

        result = EmailAgent(FakeLLM()).summarize(message)

        self.assertEqual(result.category, "homelab")
        self.assertEqual(result.priority, "high")
        self.assertEqual(len(result.action_items), 1)


if __name__ == "__main__":
    unittest.main()
