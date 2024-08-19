from wg_wrapper.config import WGInterfaceConfigWritter
from wg_wrapper.schemas import WGKeys, WGServerConfig
from wg_wrapper.wrapper import WGWrapper

from wg_service.models.wg0_key import WG0KeyModel
from wg_service.settings import settings
from wg_service.unit_of_work.unit_of_work import UnitOfWork


class WG0Service:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_wg0_keys(self) -> WG0KeyModel:
        keys = await self.uow.wg0_key.get_one()
        if keys:
            return keys
        generated_keys = await WGWrapper.gen_keys()
        return await self.uow.wg0_key.create_one(
            generated_keys.private_key, generated_keys.public_key
        )

    async def get_wg_config(self) -> WGServerConfig:
        keys = await self.get_wg0_keys()
        server_config = WGServerConfig(
            WGKeys(private_key=keys.private_key, public_key=keys.public_key),
            address="10.0.0.1/24",
            listen_port=settings.WG0_LISTEN_PORT,
            pre_up=[],
            post_up=[
                "iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o en0 -j MASQUERADE"
            ],
            pre_down=[],
            post_down=[
                "iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o en0 -j MASQUERADE"
            ],
        )
        return server_config

    async def write_default_config(self) -> None:
        server_config = await self.get_wg_config()
        WGInterfaceConfigWritter(settings.WG0_INTERFACE + ".conf").write(
            server_config, []
        )

    async def up(self) -> None:
        await WGWrapper.up()
