from ipaddress import IPv4Network

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column
from wg_wrapper.schemas import WGKeys, WGPeerConfig

from wg_service.models.base import Base
from wg_service.settings import settings


class PeerModel(Base):
    __tablename__ = "peer"
    id: Mapped[int] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column()
    public_key: Mapped[str] = mapped_column()
    allowed_ips: Mapped[IPv4Network] = mapped_column(type_=postgresql.INET)
