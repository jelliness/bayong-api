from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.product_image import ProductImageCreate


def test_product_image_create_accepts_valid_payload():
    image = ProductImageCreate(
        product_id=1,
        image_url="https://example.com/cola.jpg",
        uploaded_by="alice",
        date_added=date(2026, 1, 1),
    )

    assert image.image_url == "https://example.com/cola.jpg"


def test_product_image_create_requires_image_url():
    with pytest.raises(ValidationError):
        ProductImageCreate(product_id=1, uploaded_by="alice", date_added=date(2026, 1, 1))


def test_product_image_create_rejects_swagger_placeholder_value():
    with pytest.raises(ValidationError):
        ProductImageCreate(
            product_id=1, image_url="string", uploaded_by="alice", date_added=date(2026, 1, 1)
        )
