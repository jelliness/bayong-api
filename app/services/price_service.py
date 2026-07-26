from datetime import date
from typing import Any, Dict, Sequence

from app.models.price import Price
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.price_repository import PriceRepository


class PriceService:
    def __init__(self, price_repository: PriceRepository, price_history_repository: PriceHistoryRepository):
        self.price_repository = price_repository
        self.price_history_repository = price_history_repository

    def get(self, price_id: int) -> Price:
        return self.price_repository.get_by_id_or_raise(price_id)

    def list(self, skip: int = 0, limit: int = 100) -> Sequence[Price]:
        return self.price_repository.list(skip=skip, limit=limit)

    def create(self, data: Dict[str, Any]) -> Price:
        return self.price_repository.create(data)

    def update(self, price_id: int, data: Dict[str, Any]) -> Price:
        """Updating the price amount is logged to PriceHistory as an audit trail."""
        existing = self.price_repository.get_by_id_or_raise(price_id)
        old_price = existing.price
        updated = self.price_repository.update(price_id, data)
        if "price" in data and updated.price != old_price:
            self.price_history_repository.create(
                {
                    "product_id": updated.product_id,
                    "store_id": updated.store_id,
                    "old_price": old_price,
                    "new_price": updated.price,
                    "date_changed": date.today(),
                }
            )
        return updated

    def delete(self, price_id: int) -> None:
        self.price_repository.delete(price_id)
