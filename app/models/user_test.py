from app.models.enums import UserRole
from app.models.user import User


def test_user_persists_with_default_admin_role(db_session):
    user = User(username="alice", hashed_password="hashed")

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None
    assert user.role == UserRole.ADMIN
    assert user.created_at is not None
