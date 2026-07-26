from datetime import date
from decimal import Decimal

import pytest

from app.models.enums import PriceSource, SizeUnit
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository


@pytest.fixture()
def repo(db_session):
    return ProductRepository(db_session)


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


def test_get_by_barcode_finds_matching_product(repo):
    repo.create(_product_payload(barcode="123456"))

    found = repo.get_by_barcode("123456")

    assert found is not None
    assert found.barcode == "123456"


def test_get_by_barcode_returns_none_when_missing(repo):
    assert repo.get_by_barcode("nope") is None


def test_list_with_filters_by_category(repo):
    repo.create(_product_payload(category="Beverages", product_name="Cola"))
    repo.create(_product_payload(category="Snacks", product_name="Chips"))

    results = repo.list_with_filters(category="Beverages")

    assert [p.product_name for p in results] == ["Cola"]


def test_list_with_filters_by_brand(repo):
    repo.create(_product_payload(brand="Acme", product_name="Cola"))
    repo.create(_product_payload(brand="Other", product_name="Chips"))

    results = repo.list_with_filters(brand="Acme")

    assert [p.product_name for p in results] == ["Cola"]


def test_list_with_filters_by_tags(repo):
    repo.create(_product_payload(product_name="Vegan Cola", tags={"vegan": True}))
    repo.create(_product_payload(product_name="Regular Cola", tags={"vegan": False}))

    results = repo.list_with_filters(tags={"vegan": True})

    assert [p.product_name for p in results] == ["Vegan Cola"]


def test_get_cheapest_price_returns_lowest_priced_row(db_session, repo):
    product = repo.create(_product_payload())
    store_repo = StoreRepository(db_session)
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
    price_repo = PriceRepository(db_session)
    price_repo.create(
        dict(
            product_id=product.id,
            store_id=store.id,
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
            store_id=store.id,
            price=Decimal("45.00"),
            is_promo=False,
            membership_required=False,
            date_collected=date(2026, 1, 1),
            price_source=PriceSource.MANUAL,
        )
    )

    cheapest = repo.get_cheapest_price(product.id)

    assert cheapest.price == Decimal("45.00")


def test_get_cheapest_price_returns_none_when_no_prices(repo):
    product = repo.create(_product_payload())

    assert repo.get_cheapest_price(product.id) is None
