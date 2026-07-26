from typing import Annotated

from pydantic import AfterValidator

_PLACEHOLDER_VALUES = {"string"}


def reject_placeholder(value: str) -> str:
    """Reject FastAPI/Swagger's auto-generated example text (e.g. "string") submitted as-is."""
    if value.strip().lower() in _PLACEHOLDER_VALUES:
        raise ValueError(
            'This looks like the unedited Swagger example value ("string") - please provide a real value.'
        )
    return value


NonPlaceholderStr = Annotated[str, AfterValidator(reject_placeholder)]
