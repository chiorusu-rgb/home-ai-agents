import os
from dataclasses import dataclass
from typing import Any

from proxmoxer import ProxmoxAPI


SAFE_VMID_MIN = 900
SAFE_VMID_MAX = 999


@dataclass
class ProxmoxActionResult:
    ok: bool
    action: str
    details: dict[str, Any]
    message: str


class ProxmoxClient:
    def __init__(
        self,
        host: str | None = None,
        user: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        node: str | None = None,
        verify_ssl: bool | None = None,
        timeout: int = 30,
        allow_writes: bool = False,
    ) -> None:
        self.host = host or os.getenv("PROXMOX_HOST", "")
        self.user = user or os.getenv("PROXMOX_USER", "")
        self.token_name = token_name or os.getenv("PROXMOX_TOKEN_NAME", "")
        self.token_value = token_value or os.getenv("PROXMOX_TOKEN_VALUE", "")
        self.node = node or os.getenv("PROXMOX_NODE", "")
        self.timeout = timeout
        self.allow_writes = allow_writes
        verify_env = os.getenv("PROXMOX_VERIFY_SSL", "true").lower()
        self.verify_ssl = verify_ssl if verify_ssl is not None else (verify_env == "true")

    def _client(self) -> ProxmoxAPI:
        if not all([self.host, self.user, self.token_name, self.token_value]):
            raise RuntimeError("Proxmox credentials are not fully configured.")
        return ProxmoxAPI(
            self.host,
            user=self.user,
            token_name=self.token_name,
            token_value=self.token_value,
            verify_ssl=self.verify_ssl,
            timeout=self.timeout,
        )

    def _validate_sandbox_vmid(self, vmid: int) -> None:
        if not (SAFE_VMID_MIN <= vmid <= SAFE_VMID_MAX):
            raise ValueError(
                f"VMID {vmid} is outside the allowed sandbox range "
                f"{SAFE_VMID_MIN}-{SAFE_VMID_MAX}."
            )

    def list_nodes(self) -> list[dict[str, Any]]:
        return list(self._client().nodes.get())

    def list_lxc(self, node: str | None = None) -> list[dict[str, Any]]:
        target_node = node or self.node
        if not target_node:
            raise RuntimeError("PROXMOX_NODE is not configured.")
        return list(self._client().nodes(target_node).lxc.get())

    def create_sandbox_lxc(
        self,
        vmid: int,
        hostname: str,
        template: str = "local:vztmpl/debian-12-standard_12.2-1_amd64.tar.zst",
        memory: int = 1024,
        rootfs: str = "local-lvm:8",
        storage: str = "local-lvm",
        net0: str = "name=eth0,bridge=vmbr0,ip=dhcp",
        unprivileged: int = 1,
    ) -> ProxmoxActionResult:
        self._validate_sandbox_vmid(int(vmid))

        if not self.allow_writes:
            return ProxmoxActionResult(
                ok=False,
                action="create_sandbox_lxc",
                details={
                    "vmid": vmid,
                    "hostname": hostname,
                    "node": self.node,
                    "template": template,
                },
                message="Write operations are disabled. Proposal only.",
            )

        if not self.node:
            raise RuntimeError("PROXMOX_NODE is not configured.")

        result = self._client().nodes(self.node).lxc.post(
            vmid=int(vmid),
            hostname=f"test-{hostname}",
            ostemplate=template,
            memory=memory,
            net0=net0,
            storage=storage,
            rootfs=rootfs,
            unprivileged=unprivileged,
        )

        return ProxmoxActionResult(
            ok=True,
            action="create_sandbox_lxc",
            details={
                "vmid": vmid,
                "hostname": f"test-{hostname}",
                "node": self.node,
                "result": result,
            },
            message="Sandbox LXC creation requested.",
        )
