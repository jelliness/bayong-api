import pytest
from fastapi import HTTPException

from app.core.dependencies import get_current_user, require_admin
from app.core.security import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


def test_get_current_user_returns_user_for_valid_token(db_session):
    user = UserService(UserRepository(db_session)).create("alice", "s3cret-Pass!")
    token = create_access_token(subject=user.username, role=user.role.value)

    resolved = get_current_user(token=token, db=db_session)

    assert resolved.username == "alice"


def test_get_current_user_rejects_invalid_token(db_session):
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token="garbage", db=db_session)

    assert exc_info.value.status_code == 401


def test_get_current_user_rejects_token_for_deleted_or_unknown_user(db_session):
    token = create_access_token(subject="ghost", role="admin")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, db=db_session)

    assert exc_info.value.status_code == 401


def test_require_admin_allows_admin_role(db_session):
    user = UserService(UserRepository(db_session)).create("alice", "s3cret-Pass!")

    assert require_admin(current_user=user) is user


def test_require_admin_rejects_non_admin_role():
    non_admin = User(username="bob", hashed_password="x", role="not-admin")

    with pytest.raises(HTTPException) as exc_info:
        require_admin(current_user=non_admin)

    assert exc_info.value.status_code == 403
