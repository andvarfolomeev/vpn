from fastapi import APIRouter

from wg_service.api.v1.peer import peer_router

v1_router = APIRouter()


v1_router.include_router(peer_router)
