from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_store_service, require_admin
from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.store import StoreCreate, StoreRead, StoreUpdate
from app.services.store_service import StoreService

router = APIRouter(prefix="/stores", tags=["stores"])


@router.get("", response_model=List[StoreRead])
def list_stores(skip: int = 0, limit: int = 100, service: StoreService = Depends(get_store_service)):
    return service.list(skip=skip, limit=limit)


@router.post("", response_model=StoreRead, status_code=status.HTTP_201_CREATED)
def create_store(
    payload: StoreCreate,
    service: StoreService = Depends(get_store_service),
    _current_user: User = Depends(require_admin),
):
    return service.create(payload.model_dump())


@router.get("/{store_id}", response_model=StoreRead)
def get_store(store_id: int, service: StoreService = Depends(get_store_service)):
    try:
        return service.get(store_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{store_id}", response_model=StoreRead)
def update_store(
    store_id: int,
    payload: StoreUpdate,
    service: StoreService = Depends(get_store_service),
    _current_user: User = Depends(require_admin),
):
    try:
        return service.update(store_id, payload.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: int,
    service: StoreService = Depends(get_store_service),
    _current_user: User = Depends(require_admin),
):
    try:
        service.delete(store_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
