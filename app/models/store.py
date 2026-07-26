from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Store(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(primary_key=True)
    store_name: Mapped[str] = mapped_column(nullable=False)
    branch: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    province: Mapped[str] = mapped_column(nullable=False)
    region: Mapped[str] = mapped_column(nullable=False)
    store_type: Mapped[str] = mapped_column(nullable=False)
    has_membership: Mapped[bool] = mapped_column(default=False, nullable=False)

    prices: Mapped[List["Price"]] = relationship(back_populates="store", cascade="all, delete-orphan")
