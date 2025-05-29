import pytest
from fastapi.testclient import TestClient
from app.schemas.auth import Token # For response validation if needed, but not strictly for these tests yet

# client fixture is auto-imported by pytest from conftest.py

def test_register_user_success(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
    assert "hashed_password" not in data
    assert "password" not in data


def test_register_existing_username_fails(client: TestClient):
    # First registration
    client.post(
        "/api/v1/auth/register",
        json={"username": "existinguser", "password": "testpassword"},
    )
    # Attempt to register again with the same username
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "existinguser", "password": "anotherpassword"},
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already registered"


def test_login_success_returns_token(client: TestClient):
    # Create user first
    client.post(
        "/api/v1/auth/register",
        json={"username": "loginuser", "password": "loginpassword"},
    )
    # Attempt login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser", "password": "loginpassword"}, # OAuth2PasswordRequestForm uses form data
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password_fails(client: TestClient):
    # Create user first
    client.post(
        "/api/v1/auth/register",
        json={"username": "wrongpassuser", "password": "correctpassword"},
    )
    # Attempt login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpassuser", "password": "incorrectpassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_nonexistent_user_fails(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistentuser", "password": "anypassword"},
    )
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


# --- Tests for Protected Endpoint ---
# Using /api/v1/production/ as the sample protected endpoint

def test_access_protected_endpoint_no_token_fails(client: TestClient):
    response = client.get("/api/v1/production/")
    assert response.status_code == 401 # FastAPI's default for missing OAuth2 token
    data = response.json()
    assert data["detail"] == "Not authenticated" # Default detail for OAuth2PasswordBearer

def test_access_protected_endpoint_invalid_token_fails(client: TestClient):
    response = client.get(
        "/api/v1/production/",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401
    data = response.json()
    # This detail comes from our custom get_current_user's credentials_exception
    assert data["detail"] == "Could not validate credentials"


def test_access_protected_endpoint_valid_token_succeeds(client: TestClient):
    # 1. Register a user
    client.post(
        "/api/v1/auth/register",
        json={"username": "protectedendpointuser", "password": "testpassword"},
    )
    # 2. Login to get a token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "protectedendpointuser", "password": "testpassword"},
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]

    # 3. Access protected endpoint with the token
    response = client.get(
        "/api/v1/production/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    # The response data here would be list[ProductionRead], for now, just check success
    assert isinstance(response.json(), list)
