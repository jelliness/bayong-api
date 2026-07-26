from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.models.product_image import ProductImage


class ProductImageRepository(BaseRepository[ProductImage]):
    def __init__(self, db: Session):
        super().__init__(db, ProductImage)

    def list_by_product(self, product_id: int) -> Sequence[ProductImage]:
        stmt = select(ProductImage).where(ProductImage.product_id == product_id)
        return self.db.execute(stmt).scalars().all()
