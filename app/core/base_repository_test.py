import pytest

from app.core.base_repository import BaseRepository
from app.core.exceptions import NotFoundError
from app.models.category import Category


@pytest.fixture()
def repo(db_session):
    return BaseRepository(db_session, Category)


def test_create_persists_and_returns_entity(repo):
    category = repo.create({"category_name": "Snacks"})

    assert category.id is not None
    assert category.category_name == "Snacks"


def test_get_by_id_returns_none_when_missing(repo):
    assert repo.get_by_id(999) is None


def test_get_by_id_or_raise_raises_not_found(repo):
    with pytest.raises(NotFoundError):
        repo.get_by_id_or_raise(999)


def test_list_returns_created_entities(repo):
    repo.create({"category_name": "Snacks"})
    repo.create({"category_name": "Beverages"})

    results = repo.list()

    assert {c.category_name for c in results} == {"Snacks", "Beverages"}


def test_update_modifies_fields(repo):
    category = repo.create({"category_name": "Snacks"})

    updated = repo.update(category.id, {"category_name": "Chips"})

    assert updated.category_name == "Chips"


def test_update_raises_not_found_for_missing_id(repo):
    with pytest.raises(NotFoundError):
        repo.update(999, {"category_name": "Chips"})


def test_delete_removes_entity(repo):
    category = repo.create({"category_name": "Snacks"})

    repo.delete(category.id)

    assert repo.get_by_id(category.id) is None


def test_delete_raises_not_found_for_missing_id(repo):
    with pytest.raises(NotFoundError):
        repo.delete(999)
