from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.models.store import Store


class StoreRepository(BaseRepository[Store]):
    def __init__(self, db: Session):
        super().__init__(db, Store)

    def list_by_city(self, city: str) -> Sequence[Store]:
        stmt = select(Store).where(Store.city == city)
        return self.db.execute(stmt).scalars().all()
