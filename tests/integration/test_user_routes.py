import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from openai_api_client.main import app
from openai_api_client.dependencies.openai import OpenAIService
from openai_api_client.schemas.openai import OpenAIRequest, OpenAIResponse
from openai_api_client.services.openai import openai_service
from openai_api_client.models.user import User
from openai_api_client.schemas.user import UserCreate


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_openai():
    with patch("openai_api_client.dependencies.openai.openai") as mock_openai:
        yield mock_openai


@pytest.fixture
async def test_user(mock_user_service):
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword",
    )
    user = await mock_user_service.create_user(user_data)
    yield user
    await mock_user_service.delete_user(user.id)


class TestUserRoutes:
    def test_register_user_success(self, client):
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "testpassword",
        }
        response = client.post("/api/v1/users/register", json=user_data)
        assert response.status_code == 201
        assert response.json()["username"] == "newuser"
        assert response.json()["email"] == "newuser@example.com"
        assert response.json()["api_key"] is not None

    def test_register_user_username_exists(self, client):
        user_data = {
            "username": "testuser",
            "email": "newuser@example.com",
            "password": "testpassword",
        }
        response = client.post("/api/v1/users/register", json=user_data)
        assert response.status_code == 400
        assert "Username already exists" in response.json()["detail"]

    def test_register_user_email_exists(self, client):
        user_data = {
            "username": "newuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = client.post("/api/v1/users/register", json=user_data)
        assert response.status_code == 400
        assert "Email already exists" in response.json()["detail"]

    def test_login_user_success(self, client, test_user):
        login_data = {"email": "test@example.com", "password": "testpassword"}
        response = client.post("/api/v1/users/login", json=login_data)
        assert response.status_code == 200
        assert response.json()["access_token"] is not None
        assert response.json()["token_type"] == "bearer"

    def test_login_user_invalid_credentials(self, client, test_user):
        login_data = {"email": "test@example.com", "password": "wrongpassword"}
        response = client.post("/api/v1/users/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_get_current_user_success(self, client, test_user):
        response = client.get(
            "/api/v1/users/me", headers={"Authorization": f"Bearer {test_user.api_key}"}
        )
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
        assert response.json()["email"] == "test@example.com"
        assert response.json()["api_key"] is not None