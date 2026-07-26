from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import PriceSource
from app.schemas.store import StoreRead
from app.schemas.validators import NonPlaceholderStr


class PriceBase(BaseModel):
    product_id: int
    store_id: int
    price: Decimal
    sale_price: Optional[Decimal] = None
    is_promo: bool = False
    promo_type: Optional[str] = None
    membership_required: bool = False
    date_collected: date
    valid_until: Optional[date] = None
    price_source: PriceSource
    notes: Optional[str] = None


class PriceCreate(PriceBase):
    promo_type: Optional[NonPlaceholderStr] = None
    notes: Optional[NonPlaceholderStr] = None


class PriceUpdate(BaseModel):
    price: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    is_promo: Optional[bool] = None
    promo_type: Optional[NonPlaceholderStr] = None
    membership_required: Optional[bool] = None
    date_collected: Optional[date] = None
    valid_until: Optional[date] = None
    price_source: Optional[PriceSource] = None
    notes: Optional[NonPlaceholderStr] = None


class PriceRead(PriceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CheapestPriceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    price: PriceRead
    store: StoreRead


class PricePerUnitRead(BaseModel):
    product_id: int
    price: Decimal
    price_per_unit: Decimal
    standard_unit: str
