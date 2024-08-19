from fastapi import APIRouter

from wg_service.dependencies import UnitOfWorkDep
from wg_service.services.peer_service import PeerService

peer_router = APIRouter(prefix="/peer")


@peer_router.get("/")
async def get_peer_handler(uow: UnitOfWorkDep, public_key: str):
    async with uow:
        peer = await PeerService(uow).get_peer(public_key)
        await uow.commit()
    return peer


@peer_router.post("/")
async def post_peer_handler(uow: UnitOfWorkDep):
    async with uow:
        peer = await PeerService(uow).add_peer()
        await uow.commit()
    return peer


@peer_router.delete("/")
async def delete_peer_handler(uow: UnitOfWorkDep, public_key: str):
    async with uow:
        await PeerService(uow).delete_peer(public_key)
        await uow.commit()
    return {}


@peer_router.post("/truncate")
async def truncate_peer_handler(uow: UnitOfWorkDep):
    async with uow:
        await PeerService(uow).truncate()
    return {}
