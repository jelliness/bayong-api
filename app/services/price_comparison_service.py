from decimal import Decimal
from typing import List, Optional

from app.core.exceptions import NotFoundError
from app.models.price import Price
from app.models.price_history import PriceHistory
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository


class PriceComparisonService:
    """Derived/calculated pricing logic that spans products, prices, and stores."""

    def __init__(
        self,
        product_repository: ProductRepository,
        price_repository: PriceRepository,
        price_history_repository: PriceHistoryRepository,
    ):
        self.product_repository = product_repository
        self.price_repository = price_repository
        self.price_history_repository = price_history_repository

    def get_prices_for_product(self, product_id: int) -> List[Price]:
        """All current prices for a product across stores, cheapest (accounting for promos) first."""
        self.product_repository.get_by_id_or_raise(product_id)
        prices = self.price_repository.list_by_product(product_id)
        return sorted(prices, key=lambda p: p.effective_price())

    def get_cheapest_across_stores(self, product_id: int) -> Price:
        prices = self.get_prices_for_product(product_id)
        if not prices:
            raise NotFoundError("Price", f"for product {product_id}")
        return prices[0]

    def calculate_price_per_unit(self, product_id: int, price_value: Decimal) -> Decimal:
        product = self.product_repository.get_by_id_or_raise(product_id)
        return product.price_per_unit(price_value)

    def get_price_history(self, product_id: int, store_id: Optional[int] = None) -> List[PriceHistory]:
        self.product_repository.get_by_id_or_raise(product_id)
        return list(self.price_history_repository.list_by_product(product_id, store_id=store_id))
