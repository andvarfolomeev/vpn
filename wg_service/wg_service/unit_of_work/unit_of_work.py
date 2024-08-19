from wg_service.repositories.peer import WGPeerRepository
from wg_service.repositories.wg0_key import WG0KeyRepository
from wg_service.session import async_session_maker
from wg_service.unit_of_work.abstract import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    wg0_key: WG0KeyRepository

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        # create repositories here
        self.wg0_key = WG0KeyRepository(self.session)
        self.peer = WGPeerRepository(self.session)

    async def __aexit__(self, *_):
        await self.rollback()
        await self.session.close()

    async def rollback(self):
        await self.session.rollback()

    async def commit(self):
        await self.session.commit()
