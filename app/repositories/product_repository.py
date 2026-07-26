from typing import Dict, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.models.price import Price
from app.models.product import Product


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(db, Product)

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        stmt = select(Product).where(Product.barcode == barcode)
        return self.db.execute(stmt).scalars().first()

    def list_with_filters(
        self,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        tags: Optional[Dict[str, bool]] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Product]:
        stmt = select(Product)
        if category is not None:
            stmt = stmt.where(Product.category == category)
        if brand is not None:
            stmt = stmt.where(Product.brand == brand)
        if tags:
            for key, value in tags.items():
                stmt = stmt.where(Product.tags[key].as_boolean() == value)
        stmt = stmt.offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()

    def get_cheapest_price(self, product_id: int) -> Optional[Price]:
        """Cheapest by stored list price. Promo/sale-price logic lives in PriceComparisonService."""
        stmt = select(Price).where(Price.product_id == product_id).order_by(Price.price.asc()).limit(1)
        return self.db.execute(stmt).scalars().first()
