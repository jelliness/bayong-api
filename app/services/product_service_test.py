from datetime import date
from decimal import Decimal

import pytest

from app.core.exceptions import NotFoundError
from app.models.enums import SizeUnit
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


@pytest.fixture()
def service(db_session):
    return ProductService(ProductRepository(db_session))


def _product_payload(**overrides):
    defaults = dict(
        category="Beverages",
        subcategory="Soft Drinks",
        product_name="Cola",
        brand="Acme",
        package_type="bottle",
        size_value=Decimal("1.5"),
        size_unit=SizeUnit.L,
        standard_unit="L",
        standard_quantity=Decimal("1.5"),
        tags={},
        last_verified=date(2026, 1, 1),
    )
    defaults.update(overrides)
    return defaults


def test_create_and_get_roundtrip(service):
    product = service.create(_product_payload())

    fetched = service.get(product.id)

    assert fetched.product_name == "Cola"


def test_get_raises_not_found_for_missing_id(service):
    with pytest.raises(NotFoundError):
        service.get(999)


def test_list_filters_by_category_and_brand(service):
    service.create(_product_payload(category="Beverages", brand="Acme", product_name="Cola"))
    service.create(_product_payload(category="Snacks", brand="Other", product_name="Chips"))

    results = service.list(category="Beverages", brand="Acme")

    assert [p.product_name for p in results] == ["Cola"]


def test_update_and_delete(service):
    product = service.create(_product_payload())

    updated = service.update(product.id, {"product_name": "Cola Zero"})
    assert updated.product_name == "Cola Zero"

    service.delete(product.id)
    with pytest.raises(NotFoundError):
        service.get(product.id)
