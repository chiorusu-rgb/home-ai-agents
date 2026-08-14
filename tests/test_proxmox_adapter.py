import unittest

from src.adapters.proxmox_client import ProxmoxClient


class ProxmoxAdapterTests(unittest.TestCase):
    def test_rejects_vmid_outside_sandbox(self) -> None:
        client = ProxmoxClient(allow_writes=False)
        with self.assertRaises(ValueError):
            client._validate_sandbox_vmid(500)

    def test_allows_proposal_mode_inside_sandbox(self) -> None:
        client = ProxmoxClient(node="pve", allow_writes=False)
        result = client.create_sandbox_lxc(vmid=901, hostname="agent-test")
        self.assertFalse(result.ok)
        self.assertEqual(result.action, "create_sandbox_lxc")
        self.assertIn("Proposal only", result.message)


if __name__ == "__main__":
    unittest.main()
