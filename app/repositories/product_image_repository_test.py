from datetime import date
from decimal import Decimal

import pytest

from app.models.enums import SizeUnit
from app.repositories.product_image_repository import ProductImageRepository
from app.repositories.product_repository import ProductRepository


@pytest.fixture()
def setup(db_session):
    product_repo = ProductRepository(db_session)
    image_repo = ProductImageRepository(db_session)

    product = product_repo.create(
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
    return image_repo, product


def test_list_by_product_returns_images_for_that_product(setup):
    image_repo, product = setup
    image_repo.create(
        dict(
            product_id=product.id,
            image_url="https://example.com/cola.jpg",
            uploaded_by="alice",
            date_added=date(2026, 1, 1),
        )
    )

    results = image_repo.list_by_product(product.id)

    assert len(results) == 1
    assert results[0].image_url == "https://example.com/cola.jpg"


def test_list_by_product_returns_empty_when_none(setup):
    image_repo, product = setup

    assert image_repo.list_by_product(product.id) == []
