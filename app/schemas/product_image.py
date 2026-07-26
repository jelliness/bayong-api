from datetime import date

from pydantic import BaseModel, ConfigDict

from app.schemas.validators import NonPlaceholderStr


class ProductImageBase(BaseModel):
    product_id: int
    image_url: str
    uploaded_by: str
    date_added: date


class ProductImageCreate(ProductImageBase):
    image_url: NonPlaceholderStr
    uploaded_by: NonPlaceholderStr


class ProductImageRead(ProductImageBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
