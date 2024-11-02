from pydantic import BaseModel, validator
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @validator("username")
    def username_must_be_unique(cls, value, values):
        # Check if username is already taken (use database query)
        if User.objects.filter(username=value).exists():
            raise ValueError("Username already exists.")
        return value

    @validator("email")
    def email_must_be_unique(cls, value, values):
        # Check if email is already taken (use database query)
        if User.objects.filter(email=value).exists():
            raise ValueError("Email already exists.")
        return value

    @validator("password")
    def password_must_be_strong(cls, value):
        # Ensure password meets minimum length and complexity requirements
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit.")
        return value

class User(BaseModel):
    id: int
    username: str
    email: str
    api_key: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str