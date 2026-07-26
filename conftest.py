import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import Base

ADMIN_USERNAME = "test-admin"
ADMIN_PASSWORD = "TestPass123!"


@pytest.fixture()
def db_session():
    """A fresh in-memory SQLite database per test, isolated from real data."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture()
def client(db_session):
    """A FastAPI TestClient wired to the isolated db_session fixture instead of real Postgres."""
    from fastapi.testclient import TestClient

    from app.core.database import get_db
    from app.main import app

    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_user(db_session):
    """An admin User row created directly in the shared db_session fixture."""
    from app.repositories.user_repository import UserRepository
    from app.services.user_service import UserService

    return UserService(UserRepository(db_session)).create(ADMIN_USERNAME, ADMIN_PASSWORD)


@pytest.fixture()
def auth_headers(admin_user):
    """Bearer-token headers for the admin_user fixture, for hitting protected write endpoints."""
    from app.core.security import create_access_token

    token = create_access_token(subject=admin_user.username, role=admin_user.role.value)
    return {"Authorization": f"Bearer {token}"}
