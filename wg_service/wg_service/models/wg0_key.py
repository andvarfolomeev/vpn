from sqlalchemy.orm import Mapped, mapped_column

from wg_service.models.base import Base


class WG0KeyModel(Base):
    __tablename__ = "wg0_key"
    id: Mapped[int] = mapped_column(primary_key=True)
    private_key: Mapped[str] = mapped_column()
    public_key: Mapped[str] = mapped_column()
