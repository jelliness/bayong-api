from typing import Any, Dict, Optional, Sequence

from app.models.product import Product
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get(self, product_id: int) -> Product:
        return self.product_repository.get_by_id_or_raise(product_id)

    def list(
        self,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        tags: Optional[Dict[str, bool]] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Product]:
        return self.product_repository.list_with_filters(
            category=category, brand=brand, tags=tags, skip=skip, limit=limit
        )

    def create(self, data: Dict[str, Any]) -> Product:
        return self.product_repository.create(data)

    def update(self, product_id: int, data: Dict[str, Any]) -> Product:
        return self.product_repository.update(product_id, data)

    def delete(self, product_id: int) -> None:
        self.product_repository.delete(product_id)
