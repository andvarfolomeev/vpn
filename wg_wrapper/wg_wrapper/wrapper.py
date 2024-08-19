from wg_wrapper.command import CommandResult, run_command_zero
from wg_wrapper.schemas import CommandResult, WGKeys, WGPeerConfig


class WGWrapper:

    @classmethod
    async def up(cls) -> CommandResult:
        return await run_command_zero("wg-quick up wg0")

    @classmethod
    async def down(cls) -> CommandResult:
        return await run_command_zero("wg-quick down wg0")

    @classmethod
    async def gen_keys(cls) -> WGKeys:
        private_key = (await run_command_zero("wg genkey")).stdout.strip()
        public_key = (
            await run_command_zero(f"echo {private_key} | wg pubkey")
        ).stdout.strip()
        return WGKeys(private_key, public_key)

    @classmethod
    async def add_peer(cls, interface_name: str, peer: WGPeerConfig):
        return await run_command_zero(
            f"wg set {interface_name} peer {peer.keys.public_key.strip()} allowed-ips {peer.allowed_ips.strip()}"
        )

    @classmethod
    async def remove_peer(cls, interface_name: str, peer: WGPeerConfig):
        return await run_command_zero(
            f"wg set {interface_name} peer {peer.keys.public_key.strip()} remove"
        )

    @classmethod
    async def sync_config(cls) -> CommandResult:
        return await run_command_zero("wg syncconf wg0 <(wg-quick strip wg0)")
