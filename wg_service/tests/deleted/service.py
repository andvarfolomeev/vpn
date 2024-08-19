from ipaddress import ip_address

from fastapi import HTTPException
from wg_wrapper.schemas import WGInterfaceConfig, WGPeerConfig
from wg_wrapper.wrapper import WGWrapper

from wg_service.repositories import PeerRepository, WG0Repository
from wg_service.schemas import Peer


class WGService:
    peer_repo: PeerRepository
    wg0_repo: WG0Repository

    def __init__(self, peer_repo: PeerRepository, wg0_repo: WG0Repository):
        self.peer_repo = peer_repo
        self.wg0_repo = wg0_repo

    async def get_peer(self, public_key: str):
        peer = await self.peer_repo.get(public_key)
        if not peer:
            return HTTPException(status_code=404, detail="The peer does not exist")
        return peer

    async def create_default_wg0_config(self) -> WGInterfaceConfig:
        keys = await WGWrapper.gen_keys()
        interface = WGInterfaceConfig(
            private_key=keys.private_key,
            address="192.168.0.1",
            listen_port=5432,
            pre_up=[],
            pre_down=[],
            post_up=[
                "iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
                "ip6tables -A FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
                "sysctl -w net.ipv4.ip_forward=0",
                "sysctl -w net.ipv4.ip_forward=0",
                "iptables -A FORWARD -i wg0 -o wg0 -j REJECT",
                "iptables -D FORWARD -i wg0 -o wg0 -j REJECT",
            ],
            post_down=[
                "iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE",
                "ip6tables -D FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE",
            ],
        )
        return interface

    def peer_to_wg_peer_config(self, peer: Peer, subnet: str = "24") -> WGPeerConfig:
        ip_with_subnet = peer.allowed_ips + "/" + subnet
        return WGPeerConfig(peer.public_key, ip_with_subnet)

    async def create_peer(self) -> Peer:
        keys = await WGWrapper.gen_keys()
        last_ip = await self.peer_repo.get_last_ip() or ip_address("10.0.0.1")
        peer = Peer(
            private_key=keys.private_key,
            public_key=keys.public_key,
            allowed_ips=str(last_ip + 1),
        )
        await self.peer_repo.save(peer)
        await WGWrapper.add_peer("wg0", self.peer_to_wg_peer_config(peer))
        return peer

    async def delete_peer(self, public_key: str):
        peer = await self.peer_repo.get(public_key)
        if not peer:
            return HTTPException(status_code=404, detail="The peer does not exist")
        await WGWrapper.remove_peer("wg0", self.peer_to_wg_peer_config(peer))
