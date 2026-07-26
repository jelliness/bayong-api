from app.repositories.user_repository import UserRepository


def test_get_by_username_finds_matching_user(db_session):
    repo = UserRepository(db_session)
    repo.create({"username": "alice", "hashed_password": "hashed"})

    found = repo.get_by_username("alice")

    assert found is not None
    assert found.username == "alice"


def test_get_by_username_returns_none_when_missing(db_session):
    repo = UserRepository(db_session)

    assert repo.get_by_username("nobody") is None
