from datetime import date
from decimal import Decimal

import pytest

from app.core.exceptions import NotFoundError
from app.models.enums import PriceSource, SizeUnit
from app.repositories.price_history_repository import PriceHistoryRepository
from app.repositories.price_repository import PriceRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.store_repository import StoreRepository
from app.services.price_service import PriceService


@pytest.fixture()
def setup(db_session):
    product = ProductRepository(db_session).create(
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
    store = StoreRepository(db_session).create(
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
    price_history_repo = PriceHistoryRepository(db_session)
    service = PriceService(PriceRepository(db_session), price_history_repo)
    return service, product, store, price_history_repo


def _price_payload(product_id, store_id, **overrides):
    defaults = dict(
        product_id=product_id,
        store_id=store_id,
        price=Decimal("50.00"),
        is_promo=False,
        membership_required=False,
        date_collected=date(2026, 1, 1),
        price_source=PriceSource.MANUAL,
    )
    defaults.update(overrides)
    return defaults


def test_create_and_get_roundtrip(setup):
    service, product, store, _ = setup

    price = service.create(_price_payload(product.id, store.id))

    fetched = service.get(price.id)
    assert fetched.price == Decimal("50.00")


def test_get_raises_not_found_for_missing_id(setup):
    service, _, _, _ = setup

    with pytest.raises(NotFoundError):
        service.get(999)


def test_update_price_logs_price_history_entry(setup):
    service, product, store, history_repo = setup
    price = service.create(_price_payload(product.id, store.id, price=Decimal("50.00")))

    service.update(price.id, {"price": Decimal("45.00")})

    history = history_repo.list_by_product(product.id)
    assert len(history) == 1
    assert history[0].old_price == Decimal("50.00")
    assert history[0].new_price == Decimal("45.00")


def test_update_without_price_change_does_not_log_history(setup):
    service, product, store, history_repo = setup
    price = service.create(_price_payload(product.id, store.id, price=Decimal("50.00")))

    service.update(price.id, {"notes": "verified in-store"})

    assert history_repo.list_by_product(product.id) == []


def test_delete_removes_price(setup):
    service, product, store, _ = setup
    price = service.create(_price_payload(product.id, store.id))

    service.delete(price.id)

    with pytest.raises(NotFoundError):
        service.get(price.id)
