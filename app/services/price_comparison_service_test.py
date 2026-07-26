from datetime import date
from decimal import Decimal

import pytest

from app.core.exceptions import NotFoundError
from app.models.enums import PriceSource, SizeUnit
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository
from app.services.price_comparison_service import PriceComparisonService


@pytest.fixture()
def setup(db_session):
    product_repo = ProductRepository(db_session)
    store_repo = StoreRepository(db_session)
    price_repo = PriceRepository(db_session)
    history_repo = PriceHistoryRepository(db_session)

    product = product_repo.create(
        dict(
            category="Beverages",
            subcategory="Soft Drinks",
            product_name="Cola 1.5L",
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
    service = PriceComparisonService(product_repo, price_repo, history_repo)
    return service, price_repo, product, store_a, store_b


def _price_payload(product_id, store_id, **overrides):
    defaults = dict(
        product_id=product_id,
        store_id=store_id,
        price=Decimal("60.00"),
        is_promo=False,
        membership_required=False,
        date_collected=date(2026, 1, 1),
        price_source=PriceSource.MANUAL,
    )
    defaults.update(overrides)
    return defaults


def test_get_prices_for_product_raises_when_product_missing(setup):
    service, *_ = setup

    with pytest.raises(NotFoundError):
        service.get_prices_for_product(999)


def test_get_prices_for_product_sorts_cheapest_first_using_effective_price(setup):
    service, price_repo, product, store_a, store_b = setup
    price_repo.create(_price_payload(product.id, store_a.id, price=Decimal("60.00")))
    price_repo.create(
        _price_payload(
            product.id, store_b.id, price=Decimal("70.00"), is_promo=True, sale_price=Decimal("50.00")
        )
    )

    results = service.get_prices_for_product(product.id)

    assert [p.store_id for p in results] == [store_b.id, store_a.id]


def test_get_cheapest_across_stores_returns_lowest_effective_price(setup):
    service, price_repo, product, store_a, store_b = setup
    price_repo.create(_price_payload(product.id, store_a.id, price=Decimal("60.00")))
    price_repo.create(_price_payload(product.id, store_b.id, price=Decimal("45.00")))

    cheapest = service.get_cheapest_across_stores(product.id)

    assert cheapest.store_id == store_b.id
    assert cheapest.price == Decimal("45.00")


def test_get_cheapest_across_stores_raises_when_no_prices_exist(setup):
    service, _, product, _, _ = setup

    with pytest.raises(NotFoundError):
        service.get_cheapest_across_stores(product.id)


def test_calculate_price_per_unit(setup):
    service, _, product, _, _ = setup

    result = service.calculate_price_per_unit(product.id, Decimal("60.00"))

    assert result == Decimal("40.0000")


def test_calculate_price_per_unit_raises_when_product_missing(setup):
    service, *_ = setup

    with pytest.raises(NotFoundError):
        service.calculate_price_per_unit(999, Decimal("60.00"))


def test_get_price_history_filters_by_store(setup):
    service, _, product, store_a, store_b = setup
    history_repo = service.price_history_repository
    history_repo.create(
        dict(
            product_id=product.id,
            store_id=store_a.id,
            old_price=Decimal("55.00"),
            new_price=Decimal("60.00"),
            date_changed=date(2026, 1, 1),
        )
    )
    history_repo.create(
        dict(
            product_id=product.id,
            store_id=store_b.id,
            old_price=Decimal("40.00"),
            new_price=Decimal("45.00"),
            date_changed=date(2026, 1, 1),
        )
    )

    results = service.get_price_history(product.id, store_id=store_a.id)

    assert len(results) == 1
    assert results[0].store_id == store_a.id
