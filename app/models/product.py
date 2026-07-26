from datetime import date
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Date, Enum as SAEnum, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import SizeUnit

JSONVariant = JSONB().with_variant(SQLiteJSON(), "sqlite")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=False)
    subcategory: Mapped[str] = mapped_column(nullable=False)
    product_name: Mapped[str] = mapped_column(nullable=False)
    brand: Mapped[str] = mapped_column(nullable=False)
    variant: Mapped[Optional[str]] = mapped_column(nullable=True)
    package_type: Mapped[str] = mapped_column(nullable=False)
    size_value: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    size_unit: Mapped[SizeUnit] = mapped_column(
        SAEnum(SizeUnit, name="size_unit_enum", native_enum=True), nullable=False
    )
    pieces_per_pack: Mapped[Optional[int]] = mapped_column(nullable=True)
    standard_unit: Mapped[str] = mapped_column(nullable=False)
    standard_quantity: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    barcode: Mapped[Optional[str]] = mapped_column(nullable=True)
    manufacturer: Mapped[Optional[str]] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    availability: Mapped[bool] = mapped_column(default=True, nullable=False)
    private_label: Mapped[bool] = mapped_column(default=False, nullable=False)
    organic: Mapped[bool] = mapped_column(default=False, nullable=False)
    country_of_origin: Mapped[Optional[str]] = mapped_column(nullable=True)
    tags: Mapped[dict] = mapped_column(JSONVariant, default=dict, nullable=False)
    last_verified: Mapped[date] = mapped_column(Date, nullable=False)
    confidence_score: Mapped[Optional[float]] = mapped_column(nullable=True)

    prices: Mapped[List["Price"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    price_history: Mapped[List["PriceHistory"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    images: Mapped[List["ProductImage"]] = relationship(back_populates="product", cascade="all, delete-orphan")

    def price_per_unit(self, price: Decimal) -> Decimal:
        """Price per standard_unit/standard_quantity for a given price point (e.g. per 100g, per L)."""
        if not self.standard_quantity:
            raise ValueError("standard_quantity must be set and non-zero to compute price per unit")
        return (Decimal(price) / Decimal(self.standard_quantity)).quantize(Decimal("0.0001"))
