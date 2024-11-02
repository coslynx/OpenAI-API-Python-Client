from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .schemas.user import UserCreate, User, UserLogin, Token
from services.user import user_service
from dependencies.auth import create_access_token, get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.post("/register", response_model=User)
async def register_user(request: UserCreate):
    """
    Registers a new user.
    """
    try:
        user = await user_service.create_user(request)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(user))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error registering user: {str(e)}")

@router.post("/login", response_model=Token)
async def login_user(request: UserLogin):
    """
    Logs in a user and generates an access token.
    """
    try:
        user = await user_service.authenticate_user(request)
        access_token = create_access_token(data={"sub": user.id})
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder({"access_token": access_token, "token_type": "bearer"}))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials: {str(e)}")

@router.get("/me", response_model=User)
async def get_current_user(current_user: User = Depends(get_current_user)):
    """
    Retrieves the current user's information.
    """
    try:
        user = await user_service.get_user_by_id(current_user.id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(user))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error retrieving user: {str(e)}")