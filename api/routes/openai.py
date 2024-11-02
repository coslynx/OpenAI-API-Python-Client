from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .schemas.openai import OpenAIRequest, OpenAIResponse
from dependencies.openai import openai_service
from dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/openai", tags=["OpenAI"])

@router.post("/complete", response_model=OpenAIResponse)
async def complete_text(
    request: OpenAIRequest, 
    current_user: dict = Depends(get_current_user)
):
    """
    Completes a given text using OpenAI's text completion API.
    """
    try:
        response = await openai_service.complete_text(
            text=request.text,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return JSONResponse(
            status_code=200, 
            content=jsonable_encoder(
                {"response": response.choices[0].text}
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error completing text: {str(e)}"
        )

@router.post("/translate", response_model=OpenAIResponse)
async def translate_text(
    request: OpenAIRequest, 
    current_user: dict = Depends(get_current_user)
):
    """
    Translates a given text using OpenAI's translation API.
    """
    try:
        response = await openai_service.translate_text(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language
        )
        return JSONResponse(
            status_code=200, 
            content=jsonable_encoder(
                {"response": response.choices[0].text}
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error translating text: {str(e)}"
        )

@router.post("/summarize", response_model=OpenAIResponse)
async def summarize_text(
    request: OpenAIRequest, 
    current_user: dict = Depends(get_current_user)
):
    """
    Summarizes a given text using OpenAI's summarization API.
    """
    try:
        response = await openai_service.summarize_text(
            text=request.text,
            model=request.model
        )
        return JSONResponse(
            status_code=200, 
            content=jsonable_encoder(
                {"response": response.choices[0].text}
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error summarizing text: {str(e)}"
        )