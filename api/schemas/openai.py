from pydantic import BaseModel, validator
from typing import Optional, List

class OpenAIRequest(BaseModel):
    text: str
    model: str = "text-davinci-003"
    temperature: float = 0.7
    max_tokens: int = 256
    source_language: Optional[str] = None
    target_language: Optional[str] = None

    @validator("model")
    def model_must_be_valid(cls, value):
        valid_models = ["text-davinci-003", "text-curie-001", "text-babbage-001", "text-ada-001"]
        if value not in valid_models:
            raise ValueError("Invalid model. Choose from: " + ", ".join(valid_models))
        return value

    @validator("temperature")
    def temperature_must_be_valid(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Temperature must be between 0 and 1")
        return value

    @validator("max_tokens")
    def max_tokens_must_be_valid(cls, value):
        if value < 1 or value > 4096:
            raise ValueError("Max tokens must be between 1 and 4096")
        return value

class OpenAIResponse(BaseModel):
    response: str

class OpenAIChoice(BaseModel):
    text: str

class OpenAIUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class OpenAIModel(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str
    permissions: List[dict]
    root: str
    parent: Optional[str]
    is_moderation_model: bool
    is_text_search_model: bool
    is_translation_model: bool
    is_code_model: bool
    is_embedding_model: bool
    is_question_answering_model: bool
    is_completion_model: bool
    is_chat_completion_model: bool
    is_fine_tuned: bool
    is_available: bool