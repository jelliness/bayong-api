import pytest

from app.core.exceptions import InvalidCredentialsError
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService


@pytest.fixture()
def service(db_session):
    user_service = UserService(UserRepository(db_session))
    user_service.create("alice", "s3cret-Pass!")
    return AuthService(user_service)


def test_authenticate_succeeds_with_correct_credentials(service):
    user = service.authenticate("alice", "s3cret-Pass!")

    assert user.username == "alice"


def test_authenticate_raises_for_wrong_password(service):
    with pytest.raises(InvalidCredentialsError):
        service.authenticate("alice", "wrong-password")


def test_authenticate_raises_for_unknown_username(service):
    with pytest.raises(InvalidCredentialsError):
        service.authenticate("nobody", "whatever")


def test_create_token_embeds_username_and_role(service):
    user = service.authenticate("alice", "s3cret-Pass!")

    token = service.create_token(user)
    payload = decode_access_token(token)

    assert payload["sub"] == "alice"
    assert payload["role"] == "admin"
