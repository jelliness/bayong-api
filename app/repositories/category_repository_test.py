import pytest

from app.repositories.category_repository import CategoryRepository


@pytest.fixture()
def repo(db_session):
    return CategoryRepository(db_session)


def test_get_by_name_finds_matching_category(repo):
    repo.create({"category_name": "Snacks"})

    found = repo.get_by_name("Snacks")

    assert found is not None
    assert found.category_name == "Snacks"


def test_get_by_name_returns_none_when_missing(repo):
    assert repo.get_by_name("Unknown") is None


def test_list_by_parent_filters_by_parent_category(repo):
    repo.create({"category_name": "Chips", "parent_category": "Snacks"})
    repo.create({"category_name": "Soda", "parent_category": "Beverages"})

    results = repo.list_by_parent("Snacks")

    assert [c.category_name for c in results] == ["Chips"]
