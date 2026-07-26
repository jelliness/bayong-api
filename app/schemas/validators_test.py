import pytest
from pydantic import BaseModel, ValidationError

from app.schemas.validators import NonPlaceholderStr


class _Model(BaseModel):
    value: NonPlaceholderStr


@pytest.mark.parametrize("placeholder", ["string", "String", "  string  ", "STRING"])
def test_rejects_swagger_placeholder_value(placeholder):
    with pytest.raises(ValidationError):
        _Model(value=placeholder)


@pytest.mark.parametrize("real_value", ["Snacks", "MegaMart", "stringify", "a string of text"])
def test_accepts_real_values(real_value):
    assert _Model(value=real_value).value == real_value
