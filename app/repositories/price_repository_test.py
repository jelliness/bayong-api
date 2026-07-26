from datetime import date
from decimal import Decimal

import pytest

from app.models.enums import PriceSource, SizeUnit
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository


@pytest.fixture()
def setup(db_session):
    product_repo = ProductRepository(db_session)
    store_repo = StoreRepository(db_session)
    price_repo = PriceRepository(db_session)

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
    store_a = store_repo.create(
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
    store_b = store_repo.create(
        dict(
            store_name="ValueStore",
            branch="Uptown",
            city="Metro City",
            province="Central",
            region="Region I",
            store_type="convenience",
            has_membership=False,
        )
    )
    return price_repo, product, store_a, store_b


def test_list_by_product_returns_all_prices_for_product(setup):
    price_repo, product, store_a, store_b = setup
    price_repo.create(
        dict(
            product_id=product.id,
            store_id=store_a.id,
            price=Decimal("60.00"),
            is_promo=False,
            membership_required=False,
            date_collected=date(2026, 1, 1),
            price_source=PriceSource.MANUAL,
        )
    )
    price_repo.create(
        dict(
            product_id=product.id,
            store_id=store_b.id,
            price=Decimal("55.00"),
            is_promo=False,
            membership_required=False,
            date_collected=date(2026, 1, 1),
            price_source=PriceSource.MANUAL,
        )
    )

    results = price_repo.list_by_product(product.id)

    assert len(results) == 2


def test_list_by_store_returns_only_that_stores_prices(setup):
    price_repo, product, store_a, store_b = setup
    price_repo.create(
        dict(
            product_id=product.id,
            store_id=store_a.id,
            price=Decimal("60.00"),
            is_promo=False,
            membership_required=False,
            date_collected=date(2026, 1, 1),
            price_source=PriceSource.MANUAL,
        )
    )
    price_repo.create(
        dict(
            product_id=product.id,
            store_id=store_b.id,
            price=Decimal("55.00"),
            is_promo=False,
            membership_required=False,
            date_collected=date(2026, 1, 1),
            price_source=PriceSource.MANUAL,
        )
    )

    results = price_repo.list_by_store(store_a.id)

    assert len(results) == 1
    assert results[0].store_id == store_a.id
