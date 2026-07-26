import pytest

from app.repositories.store_repository import StoreRepository


@pytest.fixture()
def repo(db_session):
    return StoreRepository(db_session)


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


def test_list_by_city_filters_correctly(repo):
    repo.create(_store_payload(city="Metro City"))
    repo.create(_store_payload(city="Other City"))

    results = repo.list_by_city("Metro City")

    assert len(results) == 1
    assert results[0].city == "Metro City"


def test_crud_roundtrip(repo):
    store = repo.create(_store_payload())

    fetched = repo.get_by_id(store.id)
    assert fetched.store_name == "MegaMart"

    updated = repo.update(store.id, {"store_name": "MegaMart Plus"})
    assert updated.store_name == "MegaMart Plus"

    repo.delete(store.id)
    assert repo.get_by_id(store.id) is None
