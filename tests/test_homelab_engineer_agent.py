import unittest

from src.agents.homelab_engineer.service import EngineerRequest, HomelabEngineerAgent


class HomelabEngineerAgentTests(unittest.TestCase):
    def test_requires_approval_for_execution(self) -> None:
        agent = HomelabEngineerAgent()
        result = agent.run(
            EngineerRequest(
                plan="Create sandbox LXC",
                approved=False,
                target={"vmid": 901, "node": "pve"},
            )
        )
        self.assertEqual(result.mode, "proposal-only")
        self.assertFalse(result.approved)
        self.assertIsNotNone(result.blocked_reason)


if __name__ == "__main__":
    unittest.main()
