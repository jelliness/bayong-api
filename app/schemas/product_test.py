from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.product import ProductCreate, ProductUpdate


def _valid_payload(**overrides):
    defaults = dict(
        category="Beverages",
        subcategory="Soft Drinks",
        product_name="Cola",
        brand="Acme",
        package_type="bottle",
        size_value=Decimal("1.5"),
        size_unit="L",
        standard_unit="L",
        standard_quantity=Decimal("1.5"),
        last_verified=date(2026, 1, 1),
    )
    defaults.update(overrides)
    return defaults


def test_product_create_accepts_valid_payload():
    product = ProductCreate(**_valid_payload())

    assert product.product_name == "Cola"
    assert product.active is True
    assert product.tags == {}


def test_product_create_rejects_invalid_size_unit():
    with pytest.raises(ValidationError):
        ProductCreate(**_valid_payload(size_unit="invalid-unit"))


def test_product_create_requires_product_name():
    payload = _valid_payload()
    del payload["product_name"]

    with pytest.raises(ValidationError):
        ProductCreate(**payload)


def test_product_update_allows_partial_fields():
    update = ProductUpdate(product_name="Cola Zero")

    assert update.product_name == "Cola Zero"
    assert update.brand is None


def test_product_create_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        ProductCreate(**_valid_payload(brand="string"))


def test_product_update_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        ProductUpdate(product_name="string")
