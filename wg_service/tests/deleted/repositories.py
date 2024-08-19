import json
from dataclasses import asdict
from ipaddress import IPv4Address, IPv6Address, ip_address

from redis import asyncio as aioredis
from wg_wrapper.schemas import WGInterfaceConfig

from wg_service.schemas import Peer

redis = aioredis.from_url("")


class PeerRepository:
    LAST_IP_KEY: str = "last_ip_key"

    def get_key(self, public_key) -> str:
        return f"peers:{public_key}"

    async def get(self, public_key: str) -> Peer | None:
        key = self.get_key(public_key)
        peer_raw = await redis.get(key)
        if peer_raw == None:
            return peer_raw
        peer_dict = json.loads(peer_raw)
        return Peer(**peer_dict)

    async def get_last_ip(self) -> IPv4Address | IPv6Address | None:
        ip_raw = await redis.get(self.LAST_IP_KEY)
        if not ip_raw:
            return None
        return ip_address(ip_raw)

    async def save(self, peer: Peer) -> None:
        key = self.get_key(peer.public_key)
        peer_raw = peer.model_dump_json()
        await redis.set(self.LAST_IP_KEY, peer.allowed_ips)
        await redis.set(key, peer_raw)

    async def delete(self, public_key: str) -> None:
        key = self.get_key(public_key)
        await redis.delete(key)


class WG0Repository:
    KEY: str = "wg0"

    async def save(self, interface: WGInterfaceConfig) -> None:
        interface_raw = json.dumps(asdict(interface))
        await redis.set(self.KEY, interface_raw)

    async def get(self) -> WGInterfaceConfig | None:
        interface_raw = await redis.get(self.KEY)
        if not interface_raw:
            return interface_raw
        return WGInterfaceConfig(**json.loads(interface_raw))
