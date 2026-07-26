from datetime import date
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import SizeUnit
from app.schemas.validators import NonPlaceholderStr


class ProductBase(BaseModel):
    category: str
    subcategory: str
    product_name: str
    brand: str
    variant: Optional[str] = None
    package_type: str
    size_value: Decimal
    size_unit: SizeUnit
    pieces_per_pack: Optional[int] = None
    standard_unit: str
    standard_quantity: Decimal
    barcode: Optional[str] = None
    manufacturer: Optional[str] = None
    active: bool = True
    availability: bool = True
    private_label: bool = False
    organic: bool = False
    country_of_origin: Optional[str] = None
    tags: Dict[str, Any] = {}
    last_verified: date
    confidence_score: Optional[float] = None


class ProductCreate(ProductBase):
    category: NonPlaceholderStr
    subcategory: NonPlaceholderStr
    product_name: NonPlaceholderStr
    brand: NonPlaceholderStr
    variant: Optional[NonPlaceholderStr] = None
    package_type: NonPlaceholderStr
    standard_unit: NonPlaceholderStr
    barcode: Optional[NonPlaceholderStr] = None
    manufacturer: Optional[NonPlaceholderStr] = None
    country_of_origin: Optional[NonPlaceholderStr] = None


class ProductUpdate(BaseModel):
    category: Optional[NonPlaceholderStr] = None
    subcategory: Optional[NonPlaceholderStr] = None
    product_name: Optional[NonPlaceholderStr] = None
    brand: Optional[NonPlaceholderStr] = None
    variant: Optional[NonPlaceholderStr] = None
    package_type: Optional[NonPlaceholderStr] = None
    size_value: Optional[Decimal] = None
    size_unit: Optional[SizeUnit] = None
    pieces_per_pack: Optional[int] = None
    standard_unit: Optional[NonPlaceholderStr] = None
    standard_quantity: Optional[Decimal] = None
    barcode: Optional[NonPlaceholderStr] = None
    manufacturer: Optional[NonPlaceholderStr] = None
    active: Optional[bool] = None
    availability: Optional[bool] = None
    private_label: Optional[bool] = None
    organic: Optional[bool] = None
    country_of_origin: Optional[NonPlaceholderStr] = None
    tags: Optional[Dict[str, Any]] = None
    last_verified: Optional[date] = None
    confidence_score: Optional[float] = None


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
