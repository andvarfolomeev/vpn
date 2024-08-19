from fastapi import APIRouter, Depends

from wg_service.dependencies import get_service
from wg_service.schemas import Peer
from wg_service.service import WGService

router = APIRouter()


@router.post("/peer", response_model=Peer)
async def create_peer(service: WGService = Depends(get_service)):
    return await service.create_peer()
