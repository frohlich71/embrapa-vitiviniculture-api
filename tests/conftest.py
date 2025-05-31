# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.core.database import get_session
from app.main import app

DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(scope="function")
def db_session():
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def override_session(db_session):
    def _override():
        yield db_session

    app.dependency_overrides[get_session] = _override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client(override_session):
    return TestClient(app)
