from datetime import date
from decimal import Decimal

import pytest

from app.models.enums import SizeUnit
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository


@pytest.fixture()
def setup(db_session):
    product_repo = ProductRepository(db_session)
    store_repo = StoreRepository(db_session)
    history_repo = PriceHistoryRepository(db_session)

    product = product_repo.create(
        dict(
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
    )
    store = store_repo.create(
        dict(
            store_name="MegaMart",
            branch="Downtown",
            city="Metro City",
            province="Central",
            region="Region I",
            store_type="supermarket",
            has_membership=False,
        )
    )
    return history_repo, product, store


def test_list_by_product_orders_newest_first(setup):
    history_repo, product, store = setup
    history_repo.create(
        dict(
            product_id=product.id,
            store_id=store.id,
            old_price=Decimal("50.00"),
            new_price=Decimal("55.00"),
            date_changed=date(2026, 1, 1),
        )
    )
    history_repo.create(
        dict(
            product_id=product.id,
            store_id=store.id,
            old_price=Decimal("55.00"),
            new_price=Decimal("60.00"),
            date_changed=date(2026, 2, 1),
        )
    )

    results = history_repo.list_by_product(product.id)

    assert [h.new_price for h in results] == [Decimal("60.00"), Decimal("55.00")]


def test_list_by_product_filters_by_store(setup):
    history_repo, product, store = setup
    other_store = store.id + 1
    history_repo.create(
        dict(
            product_id=product.id,
            store_id=store.id,
            old_price=Decimal("50.00"),
            new_price=Decimal("55.00"),
            date_changed=date(2026, 1, 1),
        )
    )

    results = history_repo.list_by_product(product.id, store_id=other_store)

    assert results == []
