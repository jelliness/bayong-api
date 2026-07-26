from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.models.category import Category


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db, Category)

    def get_by_name(self, category_name: str) -> Optional[Category]:
        stmt = select(Category).where(Category.category_name == category_name)
        return self.db.execute(stmt).scalars().first()

    def list_by_parent(self, parent_category: Optional[str]) -> Sequence[Category]:
        stmt = select(Category).where(Category.parent_category == parent_category)
        return self.db.execute(stmt).scalars().all()
