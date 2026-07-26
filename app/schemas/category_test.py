import pytest
from pydantic import ValidationError

from app.schemas.category import CategoryCreate, CategoryUpdate


def test_category_create_accepts_valid_payload():
    category = CategoryCreate(category_name="Snacks")

    assert category.category_name == "Snacks"
    assert category.parent_category is None


def test_category_create_requires_category_name():
    with pytest.raises(ValidationError):
        CategoryCreate()


def test_category_update_allows_partial_fields():
    update = CategoryUpdate(parent_category="Beverages")

    assert update.parent_category == "Beverages"
    assert update.category_name is None


def test_category_create_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        CategoryCreate(category_name="string", parent_category="string")


def test_category_update_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        CategoryUpdate(category_name="string")
