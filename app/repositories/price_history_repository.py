from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.models.price_history import PriceHistory


class PriceHistoryRepository(BaseRepository[PriceHistory]):
    def __init__(self, db: Session):
        super().__init__(db, PriceHistory)

    def list_by_product(self, product_id: int, store_id: Optional[int] = None) -> Sequence[PriceHistory]:
        stmt = select(PriceHistory).where(PriceHistory.product_id == product_id)
        if store_id is not None:
            stmt = stmt.where(PriceHistory.store_id == store_id)
        stmt = stmt.order_by(PriceHistory.date_changed.desc())
        return self.db.execute(stmt).scalars().all()
