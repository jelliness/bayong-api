from typing import Any, Dict, Sequence

from app.models.store import Store
from app.repositories.store_repository import StoreRepository


class StoreService:
    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    def get(self, store_id: int) -> Store:
        return self.store_repository.get_by_id_or_raise(store_id)

    def list(self, skip: int = 0, limit: int = 100) -> Sequence[Store]:
        return self.store_repository.list(skip=skip, limit=limit)

    def create(self, data: Dict[str, Any]) -> Store:
        return self.store_repository.create(data)

    def update(self, store_id: int, data: Dict[str, Any]) -> Store:
        return self.store_repository.update(store_id, data)

    def delete(self, store_id: int) -> None:
        self.store_repository.delete(store_id)
