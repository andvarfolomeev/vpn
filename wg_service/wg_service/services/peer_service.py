from ipaddress import IPv4Network

from fastapi import HTTPException
from wg_wrapper.config import WGTunelConfigStrBuilder
from wg_wrapper.schemas import WGKeys, WGPeerConfig
from wg_wrapper.wrapper import WGWrapper

from wg_service.models.peer import PeerModel
from wg_service.schemas.keys import KeysSchema
from wg_service.schemas.peer import PeerSchema
from wg_service.services.wg0_service import WG0Service
from wg_service.settings import settings
from wg_service.unit_of_work.unit_of_work import UnitOfWork


class PeerService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_peer_config(self, peer: PeerModel) -> WGPeerConfig:
        return WGPeerConfig(
            WGKeys(peer.private_key, peer.public_key),
            str(peer.allowed_ips) + "/" + settings.WG_CLIENT_SUBNET,
        )

    async def get_peer_schema(self, peer_config: WGPeerConfig) -> PeerSchema:
        server_config = await WG0Service(self.uow).get_wg_config()
        config = (
            WGTunelConfigStrBuilder()
            .add_peer(server_config)
            .add_interface(peer_config)
            .build()
        )
        keys = peer_config.keys
        return PeerSchema(
            keys=KeysSchema(private_key=keys.private_key, public_key=keys.public_key),
            allowed_ips=IPv4Network(peer_config.allowed_ips),
            config=config,
        )

    async def get_peer(self, public_key: str) -> PeerSchema:
        peer = await self.uow.peer.get_one(public_key)
        if not peer:
            raise HTTPException(404, detail="Peer does not exist")
        peer_config = self.get_peer_config(peer)
        schema = await self.get_peer_schema(peer_config)
        print(schema.config)
        return schema

    async def add_existed_peers(self) -> None:
        peers = await self.uow.peer.get_many()

        for peer in peers:
            peer_config = self.get_peer_config(peer)
            await WGWrapper.add_peer(settings.WG0_INTERFACE, peer_config)

    async def add_peer(self) -> PeerSchema:
        keys = await WGWrapper.gen_keys()
        next_ip = await self.uow.peer.get_next_ip()
        peer = await self.uow.peer.create_one(
            private_key=keys.private_key,
            public_key=keys.public_key,
            allowed_ips=next_ip,
        )
        peer_config = self.get_peer_config(peer)
        await WGWrapper.add_peer(settings.WG0_INTERFACE, peer_config)
        schema = await self.get_peer_schema(peer_config)
        print(schema.config)
        return schema

    async def delete_peer(self, public_key: str) -> None:
        peer = await self.uow.peer.get_one(public_key)
        if not peer:
            raise HTTPException(404, detail="Peer does not exist")
        peer_config = self.get_peer_config(peer)
        await WGWrapper.remove_peer(settings.WG0_INTERFACE, peer_config)
        await self.uow.peer.delete_one(public_key)

    async def truncate(self) -> None:
        await self.uow.peer.delete_all()
        await WGWrapper.down()
        await WGWrapper.up()
