from typing import Any, Dict, Sequence

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get(self, category_id: int) -> Category:
        return self.category_repository.get_by_id_or_raise(category_id)

    def list(self, skip: int = 0, limit: int = 100) -> Sequence[Category]:
        return self.category_repository.list(skip=skip, limit=limit)

    def create(self, data: Dict[str, Any]) -> Category:
        return self.category_repository.create(data)

    def update(self, category_id: int, data: Dict[str, Any]) -> Category:
        return self.category_repository.update(category_id, data)

    def delete(self, category_id: int) -> None:
        self.category_repository.delete(category_id)
