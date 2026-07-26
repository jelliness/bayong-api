from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, Enum as SAEnum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import PriceSource


class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    sale_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    is_promo: Mapped[bool] = mapped_column(default=False, nullable=False)
    promo_type: Mapped[Optional[str]] = mapped_column(nullable=True)
    membership_required: Mapped[bool] = mapped_column(default=False, nullable=False)
    date_collected: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    price_source: Mapped[PriceSource] = mapped_column(
        SAEnum(PriceSource, name="price_source_enum", native_enum=True), nullable=False
    )
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)

    product: Mapped["Product"] = relationship(back_populates="prices")
    store: Mapped["Store"] = relationship(back_populates="prices")

    def effective_price(self) -> Decimal:
        """The price a shopper actually pays: the sale price while a promo is active, else the regular price."""
        if self.is_promo and self.sale_price is not None:
            return self.sale_price
        return self.price
