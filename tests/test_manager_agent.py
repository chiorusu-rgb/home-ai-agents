import unittest

from src.agents.manager.service import ManagerAgent, RouteRequest, RoutedAgent, RoutingMode


class ManagerAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = ManagerAgent()

    def test_routes_email_requests_to_email_agent(self) -> None:
        decision = self.agent.route(RouteRequest(message="Summarize my email inbox", context={}))
        self.assertEqual(decision.agent, RoutedAgent.EMAIL)
        self.assertEqual(decision.mode, RoutingMode.READ_ONLY)

    def test_routes_energy_requests_to_energy_agent(self) -> None:
        decision = self.agent.route(RouteRequest(message="Check energy and temperature", context={}))
        self.assertEqual(decision.agent, RoutedAgent.ENERGY)
        self.assertEqual(decision.mode, RoutingMode.READ_ONLY)

    def test_routes_design_requests_to_architect(self) -> None:
        decision = self.agent.route(RouteRequest(message="Design the homelab layout", context={}))
        self.assertEqual(decision.agent, RoutedAgent.HOMELAB_ARCHITECT)
        self.assertEqual(decision.mode, RoutingMode.PROPOSAL_ONLY)

    def test_routes_execution_requests_to_engineer(self) -> None:
        decision = self.agent.route(RouteRequest(message="Deploy this Proxmox change", context={}))
        self.assertEqual(decision.agent, RoutedAgent.HOMELAB_ENGINEER)
        self.assertEqual(decision.requires_approval, True)

    def test_defaults_to_architect_for_ambiguous_requests(self) -> None:
        decision = self.agent.route(RouteRequest(message="Help me with my homelab", context={}))
        self.assertEqual(decision.agent, RoutedAgent.HOMELAB_ARCHITECT)
        self.assertIsNotNone(decision.fallback)


if __name__ == "__main__":
    unittest.main()
