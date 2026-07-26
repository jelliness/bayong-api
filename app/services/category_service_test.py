import pytest

from app.core.exceptions import NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.services.category_service import CategoryService


@pytest.fixture()
def service(db_session):
    return CategoryService(CategoryRepository(db_session))


def test_create_and_get_roundtrip(service):
    category = service.create({"category_name": "Snacks"})

    fetched = service.get(category.id)

    assert fetched.category_name == "Snacks"


def test_get_raises_not_found_for_missing_id(service):
    with pytest.raises(NotFoundError):
        service.get(999)


def test_update_changes_name(service):
    category = service.create({"category_name": "Snacks"})

    updated = service.update(category.id, {"category_name": "Chips"})

    assert updated.category_name == "Chips"


def test_delete_removes_category(service):
    category = service.create({"category_name": "Snacks"})

    service.delete(category.id)

    with pytest.raises(NotFoundError):
        service.get(category.id)


def test_list_returns_all_created(service):
    service.create({"category_name": "Snacks"})
    service.create({"category_name": "Beverages"})

    results = service.list()

    assert len(results) == 2
