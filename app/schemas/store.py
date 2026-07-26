from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.validators import NonPlaceholderStr


class StoreBase(BaseModel):
    store_name: str
    branch: str
    city: str
    province: str
    region: str
    store_type: str
    has_membership: bool = False


class StoreCreate(StoreBase):
    store_name: NonPlaceholderStr
    branch: NonPlaceholderStr
    city: NonPlaceholderStr
    province: NonPlaceholderStr
    region: NonPlaceholderStr
    store_type: NonPlaceholderStr


class StoreUpdate(BaseModel):
    store_name: Optional[NonPlaceholderStr] = None
    branch: Optional[NonPlaceholderStr] = None
    city: Optional[NonPlaceholderStr] = None
    province: Optional[NonPlaceholderStr] = None
    region: Optional[NonPlaceholderStr] = None
    store_type: Optional[NonPlaceholderStr] = None
    has_membership: Optional[bool] = None


class StoreRead(StoreBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
