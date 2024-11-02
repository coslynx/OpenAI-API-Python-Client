from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import openai
from openai.error import APIError, AuthenticationError, RateLimitError, InvalidRequestError, TimeoutError, APIConnectionError
from typing import Optional, List

from dependencies.database import get_db
from dependencies.auth import get_current_user
from schemas.openai import OpenAIRequest, OpenAIResponse, OpenAIChoice, OpenAIUsage, OpenAIModel

# Load environment variables
from .config import settings

OPENAI_API_KEY = settings.openai_api_key
openai.api_key = OPENAI_API_KEY

class OpenAIService:
    """
    Service class for interacting with the OpenAI API.
    """

    async def complete_text(self, text: str, model: str = "text-davinci-003", temperature: float = 0.7, max_tokens: int = 256) -> OpenAIResponse:
        """
        Completes a given text using OpenAI's text completion API.

        Args:
            text (str): The text to be completed.
            model (str, optional): The OpenAI model to use. Defaults to "text-davinci-003".
            temperature (float, optional): The temperature parameter for controlling the randomness of the generated text. Defaults to 0.7.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 256.

        Returns:
            OpenAIResponse: The OpenAI API response containing the completed text.

        Raises:
            HTTPException: If an error occurs during the API call.
        """

        try:
            response = openai.Completion.create(
                engine=model,
                prompt=text,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return OpenAIResponse(response=response.choices[0].text)

        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI API key. Please check your API key.",
            )
        except RateLimitError:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API rate limit exceeded. Please try again later.",
            )
        except InvalidRequestError:
            raise HTTPException(
                status_code=400,
                detail="Invalid request to OpenAI API. Please check your input parameters.",
            )
        except TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Request to OpenAI API timed out. Please try again later.",
            )
        except APIConnectionError:
            raise HTTPException(
                status_code=500,
                detail="Error connecting to OpenAI API. Please check your internet connection.",
            )
        except APIError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling OpenAI API: {str(e)}",
            )

    async def translate_text(self, text: str, source_language: str, target_language: str) -> OpenAIResponse:
        """
        Translates a given text using OpenAI's translation API.

        Args:
            text (str): The text to be translated.
            source_language (str): The source language of the text.
            target_language (str): The target language to translate to.

        Returns:
            OpenAIResponse: The OpenAI API response containing the translated text.

        Raises:
            HTTPException: If an error occurs during the API call.
        """

        try:
            response = openai.Translation.create(
                model="gpt-3.5-turbo",
                from_language=source_language,
                to_language=target_language,
                text=text,
            )
            return OpenAIResponse(response=response.choices[0].text)

        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI API key. Please check your API key.",
            )
        except RateLimitError:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API rate limit exceeded. Please try again later.",
            )
        except InvalidRequestError:
            raise HTTPException(
                status_code=400,
                detail="Invalid request to OpenAI API. Please check your input parameters.",
            )
        except TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Request to OpenAI API timed out. Please try again later.",
            )
        except APIConnectionError:
            raise HTTPException(
                status_code=500,
                detail="Error connecting to OpenAI API. Please check your internet connection.",
            )
        except APIError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling OpenAI API: {str(e)}",
            )

    async def summarize_text(self, text: str, model: str = "text-davinci-003") -> OpenAIResponse:
        """
        Summarizes a given text using OpenAI's summarization API.

        Args:
            text (str): The text to be summarized.
            model (str, optional): The OpenAI model to use. Defaults to "text-davinci-003".

        Returns:
            OpenAIResponse: The OpenAI API response containing the summarized text.

        Raises:
            HTTPException: If an error occurs during the API call.
        """

        try:
            response = openai.Completion.create(
                engine=model,
                prompt=f"Summarize the following text:\n\n{text}",
                temperature=0.7,
                max_tokens=256,
            )
            return OpenAIResponse(response=response.choices[0].text)

        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI API key. Please check your API key.",
            )
        except RateLimitError:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API rate limit exceeded. Please try again later.",
            )
        except InvalidRequestError:
            raise HTTPException(
                status_code=400,
                detail="Invalid request to OpenAI API. Please check your input parameters.",
            )
        except TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Request to OpenAI API timed out. Please try again later.",
            )
        except APIConnectionError:
            raise HTTPException(
                status_code=500,
                detail="Error connecting to OpenAI API. Please check your internet connection.",
            )
        except APIError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling OpenAI API: {str(e)}",
            )

    async def get_model(self, model_id: str) -> OpenAIModel:
        """
        Retrieves information about a specific OpenAI model.

        Args:
            model_id (str): The ID of the OpenAI model to retrieve.

        Returns:
            OpenAIModel: The OpenAI model information.

        Raises:
            HTTPException: If an error occurs during the API call.
        """
        try:
            response = openai.Model.retrieve(model_id)
            return OpenAIModel(**response)
        except AuthenticationError:
            raise HTTPException(
                status_code=401,
                detail="Invalid OpenAI API key. Please check your API key.",
            )
        except RateLimitError:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API rate limit exceeded. Please try again later.",
            )
        except InvalidRequestError:
            raise HTTPException(
                status_code=400,
                detail="Invalid request to OpenAI API. Please check your input parameters.",
            )
        except TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Request to OpenAI API timed out. Please try again later.",
            )
        except APIConnectionError:
            raise HTTPException(
                status_code=500,
                detail="Error connecting to OpenAI API. Please check your internet connection.",
            )
        except APIError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error calling OpenAI API: {str(e)}",
            )


openai_service = OpenAIService()