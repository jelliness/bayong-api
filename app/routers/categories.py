from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_category_service, require_admin
from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=List[CategoryRead])
def list_categories(
    skip: int = 0, limit: int = 100, service: CategoryService = Depends(get_category_service)
):
    return service.list(skip=skip, limit=limit)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    service: CategoryService = Depends(get_category_service),
    _current_user: User = Depends(require_admin),
):
    return service.create(payload.model_dump())


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    try:
        return service.get(category_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    service: CategoryService = Depends(get_category_service),
    _current_user: User = Depends(require_admin),
):
    try:
        return service.update(category_id, payload.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    service: CategoryService = Depends(get_category_service),
    _current_user: User = Depends(require_admin),
):
    try:
        service.delete(category_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
