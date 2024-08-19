import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from wg_service.api.v1 import v1_router
from wg_service.services.peer_service import PeerService
from wg_service.services.wg0_service import WG0Service
from wg_service.settings import settings
from wg_service.unit_of_work.unit_of_work import UnitOfWork


@asynccontextmanager
async def lifespan(_):
    uow = UnitOfWork()
    async with uow:
        wg0service = WG0Service(uow)
        wgservice = PeerService(uow)
        await wg0service.write_default_config()
        await wg0service.up()
        await uow.commit()
        await wgservice.add_existed_peers()
    yield


app = FastAPI(lifespan=lifespan)  # type: ignore

app.include_router(router=v1_router)
