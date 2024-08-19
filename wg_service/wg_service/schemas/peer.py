from ipaddress import IPv4Network

from pydantic import BaseModel

from wg_service.schemas.keys import KeysSchema


class PeerSchema(BaseModel):
    keys: KeysSchema
    allowed_ips: IPv4Network
    config: str
