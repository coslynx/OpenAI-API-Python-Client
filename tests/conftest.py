import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from openai_api_client.main import app
from openai_api_client.dependencies.database import Base, get_async_session
from openai_api_client.services.user import user_service
from openai_api_client.services.openai import openai_service
from openai_api_client.models.user import User
from openai_api_client.schemas.user import UserCreate

# --- Database Setup ---

@pytest.fixture(scope="session")
async def async_session():
    async_engine = create_async_engine(
        "postgresql://user:password@host:port/database", echo=True
    )
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session

@pytest.fixture(scope="session")
async def engine():
    async_engine = create_async_engine(
        "postgresql://user:password@host:port/database", echo=True
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_engine

# --- Mock Services ---

@pytest.fixture
async def mock_user_service(async_session):
    async with user_service(db=async_session) as service:
        yield service

@pytest.fixture
async def mock_openai_service():
    async with openai_service() as service:
        yield service

# --- Test Client ---

@pytest.fixture
def client():
    return TestClient(app)

# --- Test Data ---

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