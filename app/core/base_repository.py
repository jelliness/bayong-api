from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """Shared CRUD operations for a single SQLAlchemy model.

    Entity repositories subclass this and pass their model class, then add
    entity-specific query methods on top.
    """

    def __init__(self, db: Session, model: Type[ModelT]):
        self.db = db
        self.model = model

    def get_by_id(self, id_: int) -> Optional[ModelT]:
        return self.db.get(self.model, id_)

    def get_by_id_or_raise(self, id_: int) -> ModelT:
        obj = self.get_by_id(id_)
        if obj is None:
            raise NotFoundError(self.model.__name__, id_)
        return obj

    def list(self, skip: int = 0, limit: int = 100) -> Sequence[ModelT]:
        stmt = select(self.model).offset(skip).limit(limit)
        return self.db.execute(stmt).scalars().all()

    def create(self, obj_in: Dict[str, Any]) -> ModelT:
        obj = self.model(**obj_in)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id_: int, obj_in: Dict[str, Any]) -> ModelT:
        obj = self.get_by_id_or_raise(id_)
        for field, value in obj_in.items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, id_: int) -> None:
        obj = self.get_by_id_or_raise(id_)
        self.db.delete(obj)
        self.db.commit()
