from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_price_service, require_admin
from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.price import PriceCreate, PriceRead, PriceUpdate
from app.services.price_service import PriceService

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("", response_model=List[PriceRead])
def list_prices(skip: int = 0, limit: int = 100, service: PriceService = Depends(get_price_service)):
    return service.list(skip=skip, limit=limit)


@router.post("", response_model=PriceRead, status_code=status.HTTP_201_CREATED)
def create_price(
    payload: PriceCreate,
    service: PriceService = Depends(get_price_service),
    _current_user: User = Depends(require_admin),
):
    return service.create(payload.model_dump())


@router.get("/{price_id}", response_model=PriceRead)
def get_price(price_id: int, service: PriceService = Depends(get_price_service)):
    try:
        return service.get(price_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{price_id}", response_model=PriceRead)
def update_price(
    price_id: int,
    payload: PriceUpdate,
    service: PriceService = Depends(get_price_service),
    _current_user: User = Depends(require_admin),
):
    try:
        return service.update(price_id, payload.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_price(
    price_id: int,
    service: PriceService = Depends(get_price_service),
    _current_user: User = Depends(require_admin),
):
    try:
        service.delete(price_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
