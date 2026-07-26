from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.models.price import Price


class PriceRepository(BaseRepository[Price]):
    def __init__(self, db: Session):
        super().__init__(db, Price)

    def list_by_product(self, product_id: int) -> Sequence[Price]:
        stmt = select(Price).where(Price.product_id == product_id)
        return self.db.execute(stmt).scalars().all()

    def list_by_store(self, store_id: int) -> Sequence[Price]:
        stmt = select(Price).where(Price.store_id == store_id)
        return self.db.execute(stmt).scalars().all()
