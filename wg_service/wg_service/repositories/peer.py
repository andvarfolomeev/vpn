from collections.abc import Sequence
from ipaddress import IPv4Address

from sqlalchemy import and_, delete, func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from wg_service.models.peer import PeerModel
from wg_service.repositories.abstract import Repository
from wg_service.settings import settings


class WGPeerRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_one(self, public_key: str) -> PeerModel | None:
        stmt = select(PeerModel).where(PeerModel.public_key == public_key).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_many(self) -> Sequence[PeerModel]:
        stmt = select(PeerModel)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete_one(self, public_key: str) -> None:
        print(public_key)
        stmt = delete(PeerModel).where(PeerModel.public_key == public_key)
        await self.session.execute(stmt)

    async def delete_all(self) -> None:
        stmt = delete(PeerModel)
        await self.session.execute(stmt)

    async def create_one(
        self, private_key: str, public_key: str, allowed_ips: str | IPv4Address
    ) -> PeerModel:
        stmt = (
            insert(PeerModel)
            .values(
                private_key=private_key,
                public_key=public_key,
                allowed_ips=IPv4Address(allowed_ips),
            )
            .returning(PeerModel)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_gap_ip(self):
        ips_lead = aliased(
            select(
                PeerModel.allowed_ips,
                func.lead(PeerModel.allowed_ips)
                .over(order_by=PeerModel.allowed_ips)
                .label("next_nr"),
            ).subquery(),
            name="ips_lead",
        )
        stmt = (
            select(
                (ips_lead.c.allowed_ips + 1).label("ip"),
                (ips_lead.c.next_nr - 1).label("end"),
            )
            .filter(and_(ips_lead.c.allowed_ips + 1 != ips_lead.c.next_nr))
            .limit(1)
        )
        res = (await self.session.execute(stmt)).first()
        if res and res[0]:
            return IPv4Address(res[0])
        return None

    async def get_max_ip_plus_one(self):
        stmt = select(func.max(PeerModel.allowed_ips) + 1)
        res = (await self.session.execute(stmt)).first()
        if res and res[0]:
            return IPv4Address(res[0])
        return None

    async def get_next_ip(self) -> IPv4Address:
        gap_ip = await self.get_gap_ip()
        if gap_ip:
            return gap_ip
        max_ip = await self.get_max_ip_plus_one()
        if max_ip:
            return max_ip
        return IPv4Address(settings.WG_START_CLIENT_IP)
