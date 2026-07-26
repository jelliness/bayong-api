from datetime import date
from decimal import Decimal

from app.schemas.price_history import PriceHistoryRead


def test_price_history_read_builds_from_orm_like_object():
    class FakeOrmRow:
        id = 1
        product_id = 2
        store_id = 3
        old_price = Decimal("50.00")
        new_price = Decimal("45.00")
        date_changed = date(2026, 1, 1)

    read = PriceHistoryRead.model_validate(FakeOrmRow())

    assert read.old_price == Decimal("50.00")
    assert read.new_price == Decimal("45.00")
