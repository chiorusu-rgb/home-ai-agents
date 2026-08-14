import unittest

from src.agents.homelab_architect.service import ArchitectRequest, HomelabArchitectAgent


class HomelabArchitectAgentTests(unittest.TestCase):
    def test_returns_proposal_only_result(self) -> None:
        agent = HomelabArchitectAgent()
        result = agent.run(
            ArchitectRequest(
                goal="Deploy a test automation service",
                constraints=["sandbox only", "no production VMIDs 100-500"],
                inventory={"platform": "Proxmox"},
            )
        )
        self.assertEqual(result.mode, "proposal-only")
        self.assertIn("safe homelab plan", result.proposal.lower())
        self.assertTrue(result.risks)


if __name__ == "__main__":
    unittest.main()
