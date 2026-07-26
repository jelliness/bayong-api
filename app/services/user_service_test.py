from app.core.security import verify_password
from app.models.enums import UserRole
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def test_create_hashes_the_password(db_session):
    service = UserService(UserRepository(db_session))

    user = service.create("alice", "s3cret-Pass!")

    assert user.hashed_password != "s3cret-Pass!"
    assert verify_password("s3cret-Pass!", user.hashed_password) is True
    assert user.role == UserRole.ADMIN


def test_get_by_username_returns_created_user(db_session):
    service = UserService(UserRepository(db_session))
    service.create("alice", "s3cret-Pass!")

    found = service.get_by_username("alice")

    assert found is not None
    assert found.username == "alice"


def test_get_by_username_returns_none_when_missing(db_session):
    service = UserService(UserRepository(db_session))

    assert service.get_by_username("nobody") is None
