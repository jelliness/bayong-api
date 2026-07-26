from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.price import PriceCreate, PriceUpdate


def _valid_payload(**overrides):
    defaults = dict(
        product_id=1,
        store_id=1,
        price=Decimal("50.00"),
        date_collected=date(2026, 1, 1),
        price_source="manual",
    )
    defaults.update(overrides)
    return defaults


def test_price_create_accepts_valid_payload():
    price = PriceCreate(**_valid_payload())

    assert price.price == Decimal("50.00")
    assert price.is_promo is False


def test_price_create_rejects_invalid_price_source():
    with pytest.raises(ValidationError):
        PriceCreate(**_valid_payload(price_source="not-a-source"))


def test_price_create_requires_price_field():
    payload = _valid_payload()
    del payload["price"]

    with pytest.raises(ValidationError):
        PriceCreate(**payload)


def test_price_update_allows_partial_fields():
    update = PriceUpdate(price=Decimal("45.00"))

    assert update.price == Decimal("45.00")
    assert update.notes is None


def test_price_create_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        PriceCreate(**_valid_payload(notes="string"))


def test_price_update_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        PriceUpdate(promo_type="string")
