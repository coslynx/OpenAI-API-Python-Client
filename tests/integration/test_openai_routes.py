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


class TestOpenAIRoutes:
    def test_complete_text_success(self, client, mock_openai, test_user):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="This is the completed text.")],
        )
        request = OpenAIRequest(text="This is the prompt.")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 200
        assert response.json() == {"response": "This is the completed text."}
        mock_openai.Completion.create.assert_called_once_with(
            engine=request.model,
            prompt=request.text,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

    def test_complete_text_invalid_model(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.InvalidRequestError(
            "Invalid model."
        )
        request = OpenAIRequest(text="This is the prompt.", model="invalid_model")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 400
        assert "Invalid request to OpenAI API" in response.json()["detail"]

    def test_complete_text_rate_limit(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.RateLimitError(
            "Rate limit exceeded."
        )
        request = OpenAIRequest(text="This is the prompt.")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 429
        assert "OpenAI API rate limit exceeded" in response.json()["detail"]

    def test_complete_text_authentication_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.AuthenticationError(
            "Invalid API key."
        )
        request = OpenAIRequest(text="This is the prompt.")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 401
        assert "Invalid OpenAI API key" in response.json()["detail"]

    def test_complete_text_timeout_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.TimeoutError(
            "Request timed out."
        )
        request = OpenAIRequest(text="This is the prompt.")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 504
        assert "Request to OpenAI API timed out" in response.json()["detail"]

    def test_complete_text_connection_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.APIConnectionError(
            "Connection error."
        )
        request = OpenAIRequest(text="This is the prompt.")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 500
        assert "Error connecting to OpenAI API" in response.json()["detail"]

    def test_complete_text_general_api_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.APIError(
            "General API error."
        )
        request = OpenAIRequest(text="This is the prompt.")
        response = client.post(
            "/api/v1/openai/complete",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 500
        assert "Error calling OpenAI API" in response.json()["detail"]

    def test_translate_text_success(self, client, mock_openai, test_user):
        mock_openai.Translation.create.return_value = MagicMock(
            choices=[MagicMock(text="This is the translated text.")],
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="en",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 200
        assert response.json() == {"response": "This is the translated text."}
        mock_openai.Translation.create.assert_called_once_with(
            model="gpt-3.5-turbo",
            from_language="en",
            to_language="fr",
            text="This is the text to translate.",
        )

    def test_translate_text_invalid_request(self, client, mock_openai, test_user):
        mock_openai.Translation.create.side_effect = openai.error.InvalidRequestError(
            "Invalid request."
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="invalid",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 400
        assert "Invalid request to OpenAI API" in response.json()["detail"]

    def test_translate_text_rate_limit(self, client, mock_openai, test_user):
        mock_openai.Translation.create.side_effect = openai.error.RateLimitError(
            "Rate limit exceeded."
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="en",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 429
        assert "OpenAI API rate limit exceeded" in response.json()["detail"]

    def test_translate_text_authentication_error(
        self, client, mock_openai, test_user
    ):
        mock_openai.Translation.create.side_effect = openai.error.AuthenticationError(
            "Invalid API key."
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="en",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 401
        assert "Invalid OpenAI API key" in response.json()["detail"]

    def test_translate_text_timeout_error(self, client, mock_openai, test_user):
        mock_openai.Translation.create.side_effect = openai.error.TimeoutError(
            "Request timed out."
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="en",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 504
        assert "Request to OpenAI API timed out" in response.json()["detail"]

    def test_translate_text_connection_error(self, client, mock_openai, test_user):
        mock_openai.Translation.create.side_effect = openai.error.APIConnectionError(
            "Connection error."
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="en",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 500
        assert "Error connecting to OpenAI API" in response.json()["detail"]

    def test_translate_text_general_api_error(self, client, mock_openai, test_user):
        mock_openai.Translation.create.side_effect = openai.error.APIError(
            "General API error."
        )
        request = OpenAIRequest(
            text="This is the text to translate.",
            source_language="en",
            target_language="fr",
        )
        response = client.post(
            "/api/v1/openai/translate",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 500
        assert "Error calling OpenAI API" in response.json()["detail"]

    def test_summarize_text_success(self, client, mock_openai, test_user):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="This is the summarized text.")],
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 200
        assert response.json() == {"response": "This is the summarized text."}
        mock_openai.Completion.create.assert_called_once_with(
            engine=request.model,
            prompt=f"Summarize the following text:\n\n{request.text}",
            temperature=0.7,
            max_tokens=256,
        )

    def test_summarize_text_invalid_request(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.InvalidRequestError(
            "Invalid request."
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 400
        assert "Invalid request to OpenAI API" in response.json()["detail"]

    def test_summarize_text_rate_limit(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.RateLimitError(
            "Rate limit exceeded."
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 429
        assert "OpenAI API rate limit exceeded" in response.json()["detail"]

    def test_summarize_text_authentication_error(
        self, client, mock_openai, test_user
    ):
        mock_openai.Completion.create.side_effect = openai.error.AuthenticationError(
            "Invalid API key."
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 401
        assert "Invalid OpenAI API key" in response.json()["detail"]

    def test_summarize_text_timeout_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.TimeoutError(
            "Request timed out."
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 504
        assert "Request to OpenAI API timed out" in response.json()["detail"]

    def test_summarize_text_connection_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.APIConnectionError(
            "Connection error."
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 500
        assert "Error connecting to OpenAI API" in response.json()["detail"]

    def test_summarize_text_general_api_error(self, client, mock_openai, test_user):
        mock_openai.Completion.create.side_effect = openai.error.APIError(
            "General API error."
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        response = client.post(
            "/api/v1/openai/summarize",
            json=request.dict(),
            headers={"Authorization": f"Bearer {test_user.api_key}"},
        )
        assert response.status_code == 500
        assert "Error calling OpenAI API" in response.json()["detail"]