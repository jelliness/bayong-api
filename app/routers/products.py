from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.dependencies import get_price_comparison_service, get_product_service, require_admin
from app.core.exceptions import NotFoundError
from app.models.user import User
from app.schemas.price import CheapestPriceRead, PriceRead
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.price_comparison_service import PriceComparisonService
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])

_KNOWN_QUERY_PARAMS = {"category", "brand", "skip", "limit"}


@router.get("", response_model=List[ProductRead])
def list_products(
    request: Request,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    service: ProductService = Depends(get_product_service),
):
    """Tag filters are passed as arbitrary query params, e.g. ?vegan=true&gluten_free=false."""
    tags = {
        key: value.lower() == "true"
        for key, value in request.query_params.items()
        if key not in _KNOWN_QUERY_PARAMS
    }
    return service.list(category=category, brand=brand, tags=tags or None, skip=skip, limit=limit)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    service: ProductService = Depends(get_product_service),
    _current_user: User = Depends(require_admin),
):
    return service.create(payload.model_dump())


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    try:
        return service.get(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    service: ProductService = Depends(get_product_service),
    _current_user: User = Depends(require_admin),
):
    try:
        return service.update(product_id, payload.model_dump(exclude_unset=True))
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
    _current_user: User = Depends(require_admin),
):
    try:
        service.delete(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{product_id}/prices", response_model=List[PriceRead])
def list_product_prices(
    product_id: int, service: PriceComparisonService = Depends(get_price_comparison_service)
):
    try:
        return service.get_prices_for_product(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{product_id}/cheapest", response_model=CheapestPriceRead)
def get_cheapest_price(
    product_id: int, service: PriceComparisonService = Depends(get_price_comparison_service)
):
    try:
        cheapest = service.get_cheapest_across_stores(product_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return CheapestPriceRead.model_validate({"price": cheapest, "store": cheapest.store})
