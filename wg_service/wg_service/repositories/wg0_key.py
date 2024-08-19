from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from wg_service.models.wg0_key import WG0KeyModel
from wg_service.repositories.abstract import Repository


class WG0KeyRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_one(self) -> WG0KeyModel | None:
        stmt = select(WG0KeyModel).limit(1).order_by(WG0KeyModel.id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_one(self, private_key: str, public_key: str) -> WG0KeyModel:
        stmt = (
            insert(WG0KeyModel)
            .values(private_key=private_key, public_key=public_key)
            .returning(WG0KeyModel)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one()
