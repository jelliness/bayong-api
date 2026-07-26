from app.schemas.user import Token


def test_token_defaults_to_bearer_type():
    token = Token(access_token="abc123")

    assert token.token_type == "bearer"
    assert token.access_token == "abc123"
