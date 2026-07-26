from datetime import date
from decimal import Decimal

import pytest

from app.models.enums import SizeUnit
from app.models.product import Product


def _make_product(**overrides) -> Product:
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
        active=True,
        availability=True,
        private_label=False,
        organic=False,
        tags={},
        last_verified=date(2026, 1, 1),
    )
    defaults.update(overrides)
    return Product(**defaults)


def test_price_per_unit_computes_price_divided_by_standard_quantity():
    product = _make_product(standard_quantity=Decimal("2"))

    result = product.price_per_unit(Decimal("10"))

    assert result == Decimal("5.0000")


def test_price_per_unit_raises_when_standard_quantity_is_zero():
    product = _make_product(standard_quantity=Decimal("0"))

    with pytest.raises(ValueError):
        product.price_per_unit(Decimal("10"))


def test_product_persists_and_defaults_relationships_empty(db_session):
    product = _make_product()

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    assert product.id is not None
    assert product.prices == []
    assert product.images == []
