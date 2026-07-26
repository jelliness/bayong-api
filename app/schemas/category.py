from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.validators import NonPlaceholderStr


class CategoryBase(BaseModel):
    category_name: str
    parent_category: Optional[str] = None


class CategoryCreate(CategoryBase):
    category_name: NonPlaceholderStr
    parent_category: Optional[NonPlaceholderStr] = None


class CategoryUpdate(BaseModel):
    category_name: Optional[NonPlaceholderStr] = None
    parent_category: Optional[NonPlaceholderStr] = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
