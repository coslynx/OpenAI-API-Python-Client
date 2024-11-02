import pytest
from fastapi import HTTPException, status
from unittest.mock import patch, MagicMock

from openai_api_client.dependencies.openai import OpenAIService, openai_service
from openai_api_client.schemas.openai import OpenAIRequest, OpenAIResponse, OpenAIModel

# Mocking the OpenAI library for unit testing
@pytest.fixture
def mock_openai():
    with patch("openai_api_client.dependencies.openai.openai") as mock_openai:
        yield mock_openai

# Test cases for text completion
class TestOpenAI_CompleteText:
    def test_complete_text_success(self, mock_openai):
        """Test successful text completion with valid parameters."""
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="This is the completed text.")],
        )
        request = OpenAIRequest(text="This is the prompt.")
        service = OpenAIService()
        response = service.complete_text(text=request.text)
        assert response.response == "This is the completed text."
        mock_openai.Completion.create.assert_called_once_with(
            engine=request.model, prompt=request.text, temperature=request.temperature, max_tokens=request.max_tokens
        )

    def test_complete_text_invalid_model(self, mock_openai):
        """Test handling of invalid OpenAI model."""
        mock_openai.Completion.create.side_effect = openai.error.InvalidRequestError("Invalid model.")
        request = OpenAIRequest(text="This is the prompt.", model="invalid_model")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.complete_text(text=request.text, model=request.model)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid request to OpenAI API" in str(exc.value.detail)

    def test_complete_text_rate_limit(self, mock_openai):
        """Test handling of OpenAI API rate limit."""
        mock_openai.Completion.create.side_effect = openai.error.RateLimitError("Rate limit exceeded.")
        request = OpenAIRequest(text="This is the prompt.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.complete_text(text=request.text)
        assert exc.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "OpenAI API rate limit exceeded" in str(exc.value.detail)

    def test_complete_text_authentication_error(self, mock_openai):
        """Test handling of authentication error with OpenAI API."""
        mock_openai.Completion.create.side_effect = openai.error.AuthenticationError("Invalid API key.")
        request = OpenAIRequest(text="This is the prompt.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.complete_text(text=request.text)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid OpenAI API key" in str(exc.value.detail)

    def test_complete_text_timeout_error(self, mock_openai):
        """Test handling of timeout error during API call."""
        mock_openai.Completion.create.side_effect = openai.error.TimeoutError("Request timed out.")
        request = OpenAIRequest(text="This is the prompt.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.complete_text(text=request.text)
        assert exc.value.status_code == status.HTTP_504_GATEWAY_TIMEOUT
        assert "Request to OpenAI API timed out" in str(exc.value.detail)

    def test_complete_text_connection_error(self, mock_openai):
        """Test handling of connection error with OpenAI API."""
        mock_openai.Completion.create.side_effect = openai.error.APIConnectionError("Connection error.")
        request = OpenAIRequest(text="This is the prompt.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.complete_text(text=request.text)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error connecting to OpenAI API" in str(exc.value.detail)

    def test_complete_text_general_api_error(self, mock_openai):
        """Test handling of general API error during call."""
        mock_openai.Completion.create.side_effect = openai.error.APIError("General API error.")
        request = OpenAIRequest(text="This is the prompt.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.complete_text(text=request.text)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error calling OpenAI API" in str(exc.value.detail)

# Test cases for text translation
class TestOpenAI_TranslateText:
    def test_translate_text_success(self, mock_openai):
        """Test successful text translation with valid parameters."""
        mock_openai.Translation.create.return_value = MagicMock(
            choices=[MagicMock(text="This is the translated text.")],
        )
        request = OpenAIRequest(text="This is the text to translate.", source_language="en", target_language="fr")
        service = OpenAIService()
        response = service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert response.response == "This is the translated text."
        mock_openai.Translation.create.assert_called_once_with(
            model="gpt-3.5-turbo", from_language="en", to_language="fr", text="This is the text to translate."
        )

    def test_translate_text_invalid_request(self, mock_openai):
        """Test handling of invalid request for translation."""
        mock_openai.Translation.create.side_effect = openai.error.InvalidRequestError("Invalid request.")
        request = OpenAIRequest(text="This is the text to translate.", source_language="invalid", target_language="fr")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid request to OpenAI API" in str(exc.value.detail)

    def test_translate_text_rate_limit(self, mock_openai):
        """Test handling of OpenAI API rate limit during translation."""
        mock_openai.Translation.create.side_effect = openai.error.RateLimitError("Rate limit exceeded.")
        request = OpenAIRequest(text="This is the text to translate.", source_language="en", target_language="fr")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert exc.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "OpenAI API rate limit exceeded" in str(exc.value.detail)

    def test_translate_text_authentication_error(self, mock_openai):
        """Test handling of authentication error during translation."""
        mock_openai.Translation.create.side_effect = openai.error.AuthenticationError("Invalid API key.")
        request = OpenAIRequest(text="This is the text to translate.", source_language="en", target_language="fr")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid OpenAI API key" in str(exc.value.detail)

    def test_translate_text_timeout_error(self, mock_openai):
        """Test handling of timeout error during translation."""
        mock_openai.Translation.create.side_effect = openai.error.TimeoutError("Request timed out.")
        request = OpenAIRequest(text="This is the text to translate.", source_language="en", target_language="fr")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert exc.value.status_code == status.HTTP_504_GATEWAY_TIMEOUT
        assert "Request to OpenAI API timed out" in str(exc.value.detail)

    def test_translate_text_connection_error(self, mock_openai):
        """Test handling of connection error during translation."""
        mock_openai.Translation.create.side_effect = openai.error.APIConnectionError("Connection error.")
        request = OpenAIRequest(text="This is the text to translate.", source_language="en", target_language="fr")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error connecting to OpenAI API" in str(exc.value.detail)

    def test_translate_text_general_api_error(self, mock_openai):
        """Test handling of general API error during translation."""
        mock_openai.Translation.create.side_effect = openai.error.APIError("General API error.")
        request = OpenAIRequest(text="This is the text to translate.", source_language="en", target_language="fr")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.translate_text(text=request.text, source_language=request.source_language, target_language=request.target_language)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error calling OpenAI API" in str(exc.value.detail)

# Test cases for text summarization
class TestOpenAI_SummarizeText:
    def test_summarize_text_success(self, mock_openai):
        """Test successful text summarization with valid parameters."""
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="This is the summarized text.")],
        )
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        response = service.summarize_text(text=request.text)
        assert response.response == "This is the summarized text."
        mock_openai.Completion.create.assert_called_once_with(
            engine=request.model, prompt=f"Summarize the following text:\n\n{request.text}", temperature=0.7, max_tokens=256
        )

    def test_summarize_text_invalid_request(self, mock_openai):
        """Test handling of invalid request for summarization."""
        mock_openai.Completion.create.side_effect = openai.error.InvalidRequestError("Invalid request.")
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.summarize_text(text=request.text)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid request to OpenAI API" in str(exc.value.detail)

    def test_summarize_text_rate_limit(self, mock_openai):
        """Test handling of OpenAI API rate limit during summarization."""
        mock_openai.Completion.create.side_effect = openai.error.RateLimitError("Rate limit exceeded.")
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.summarize_text(text=request.text)
        assert exc.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "OpenAI API rate limit exceeded" in str(exc.value.detail)

    def test_summarize_text_authentication_error(self, mock_openai):
        """Test handling of authentication error during summarization."""
        mock_openai.Completion.create.side_effect = openai.error.AuthenticationError("Invalid API key.")
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.summarize_text(text=request.text)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid OpenAI API key" in str(exc.value.detail)

    def test_summarize_text_timeout_error(self, mock_openai):
        """Test handling of timeout error during summarization."""
        mock_openai.Completion.create.side_effect = openai.error.TimeoutError("Request timed out.")
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.summarize_text(text=request.text)
        assert exc.value.status_code == status.HTTP_504_GATEWAY_TIMEOUT
        assert "Request to OpenAI API timed out" in str(exc.value.detail)

    def test_summarize_text_connection_error(self, mock_openai):
        """Test handling of connection error during summarization."""
        mock_openai.Completion.create.side_effect = openai.error.APIConnectionError("Connection error.")
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.summarize_text(text=request.text)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error connecting to OpenAI API" in str(exc.value.detail)

    def test_summarize_text_general_api_error(self, mock_openai):
        """Test handling of general API error during summarization."""
        mock_openai.Completion.create.side_effect = openai.error.APIError("General API error.")
        request = OpenAIRequest(text="This is the text to summarize.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.summarize_text(text=request.text)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error calling OpenAI API" in str(exc.value.detail)

# Test cases for model retrieval
class TestOpenAI_GetModel:
    def test_get_model_success(self, mock_openai):
        """Test successful model retrieval with valid model ID."""
        mock_openai.Model.retrieve.return_value = MagicMock(
            id="model-id",
            object="model",
            created=1678886400,
            owned_by="user-id",
            permissions=[{"id": "permission-id", "allow": ["fine-tune", "use"], "created": 1678886400}],
            root="model-id",
            parent="model-id",
            is_moderation_model=False,
            is_text_search_model=False,
            is_translation_model=False,
            is_code_model=False,
            is_embedding_model=False,
            is_question_answering_model=False,
            is_completion_model=True,
            is_chat_completion_model=False,
            is_fine_tuned=False,
            is_available=True,
        )
        service = OpenAIService()
        response = service.get_model(model_id="model-id")
        assert response.id == "model-id"
        assert response.is_completion_model
        assert response.is_available
        mock_openai.Model.retrieve.assert_called_once_with("model-id")

    def test_get_model_invalid_model_id(self, mock_openai):
        """Test handling of invalid model ID."""
        mock_openai.Model.retrieve.side_effect = openai.error.InvalidRequestError("Invalid model ID.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.get_model(model_id="invalid-model-id")
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid request to OpenAI API" in str(exc.value.detail)

    def test_get_model_rate_limit(self, mock_openai):
        """Test handling of OpenAI API rate limit during model retrieval."""
        mock_openai.Model.retrieve.side_effect = openai.error.RateLimitError("Rate limit exceeded.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.get_model(model_id="model-id")
        assert exc.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "OpenAI API rate limit exceeded" in str(exc.value.detail)

    def test_get_model_authentication_error(self, mock_openai):
        """Test handling of authentication error during model retrieval."""
        mock_openai.Model.retrieve.side_effect = openai.error.AuthenticationError("Invalid API key.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.get_model(model_id="model-id")
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid OpenAI API key" in str(exc.value.detail)

    def test_get_model_timeout_error(self, mock_openai):
        """Test handling of timeout error during model retrieval."""
        mock_openai.Model.retrieve.side_effect = openai.error.TimeoutError("Request timed out.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.get_model(model_id="model-id")
        assert exc.value.status_code == status.HTTP_504_GATEWAY_TIMEOUT
        assert "Request to OpenAI API timed out" in str(exc.value.detail)

    def test_get_model_connection_error(self, mock_openai):
        """Test handling of connection error during model retrieval."""
        mock_openai.Model.retrieve.side_effect = openai.error.APIConnectionError("Connection error.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.get_model(model_id="model-id")
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error connecting to OpenAI API" in str(exc.value.detail)

    def test_get_model_general_api_error(self, mock_openai):
        """Test handling of general API error during model retrieval."""
        mock_openai.Model.retrieve.side_effect = openai.error.APIError("General API error.")
        service = OpenAIService()
        with pytest.raises(HTTPException) as exc:
            service.get_model(model_id="model-id")
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error calling OpenAI API" in str(exc.value.detail)