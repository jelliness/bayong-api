import pytest

from app.core.exceptions import NotFoundError
from app.repositories.store_repository import StoreRepository
from app.services.store_service import StoreService


@pytest.fixture()
def service(db_session):
    return StoreService(StoreRepository(db_session))


def _store_payload(**overrides):
    defaults = dict(
        store_name="MegaMart",
        branch="Downtown",
        city="Metro City",
        province="Central",
        region="Region I",
        store_type="supermarket",
        has_membership=False,
    )
    defaults.update(overrides)
    return defaults


def test_create_and_get_roundtrip(service):
    store = service.create(_store_payload())

    fetched = service.get(store.id)

    assert fetched.store_name == "MegaMart"


def test_get_raises_not_found_for_missing_id(service):
    with pytest.raises(NotFoundError):
        service.get(999)


def test_update_changes_fields(service):
    store = service.create(_store_payload())

    updated = service.update(store.id, {"store_name": "MegaMart Plus"})

    assert updated.store_name == "MegaMart Plus"


def test_delete_removes_store(service):
    store = service.create(_store_payload())

    service.delete(store.id)

    with pytest.raises(NotFoundError):
        service.get(store.id)
