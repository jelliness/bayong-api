import pytest
from pydantic import ValidationError

from app.schemas.store import StoreCreate, StoreUpdate


def _valid_payload(**overrides):
    defaults = dict(
        store_name="MegaMart",
        branch="Downtown",
        city="Metro City",
        province="Central",
        region="Region I",
        store_type="supermarket",
    )
    defaults.update(overrides)
    return defaults


def test_store_create_accepts_valid_payload():
    store = StoreCreate(**_valid_payload())

    assert store.store_name == "MegaMart"
    assert store.has_membership is False


def test_store_create_requires_store_name():
    payload = _valid_payload()
    del payload["store_name"]

    with pytest.raises(ValidationError):
        StoreCreate(**payload)


def test_store_update_allows_partial_fields():
    update = StoreUpdate(has_membership=True)

    assert update.has_membership is True
    assert update.store_name is None


def test_store_create_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        StoreCreate(**_valid_payload(store_name="string"))


def test_store_update_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        StoreUpdate(city="string")
