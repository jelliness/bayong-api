from datetime import date
from decimal import Decimal

from app.models.enums import PriceSource
from app.models.price import Price


def _make_price(**overrides) -> Price:
    defaults = dict(
        product_id=1,
        store_id=1,
        price=Decimal("100.00"),
        is_promo=False,
        membership_required=False,
        date_collected=date(2026, 1, 1),
        price_source=PriceSource.MANUAL,
    )
    defaults.update(overrides)
    return Price(**defaults)


def test_effective_price_returns_regular_price_when_not_promo():
    price = _make_price(price=Decimal("100.00"), is_promo=False, sale_price=Decimal("80.00"))

    assert price.effective_price() == Decimal("100.00")


def test_effective_price_returns_sale_price_when_promo_active():
    price = _make_price(price=Decimal("100.00"), is_promo=True, sale_price=Decimal("80.00"))

    assert price.effective_price() == Decimal("80.00")


def test_effective_price_falls_back_to_regular_price_when_promo_has_no_sale_price():
    price = _make_price(price=Decimal("100.00"), is_promo=True, sale_price=None)

    assert price.effective_price() == Decimal("100.00")
