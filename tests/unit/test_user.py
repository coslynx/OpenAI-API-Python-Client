import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from openai_api_client.dependencies.auth import create_access_token
from openai_api_client.dependencies.database import get_db
from openai_api_client.models.user import User
from openai_api_client.schemas.user import UserCreate, User, UserLogin, Token
from openai_api_client.services.user import user_service

# Load environment variables
from openai_api_client.config import settings

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mock the database session for unit testing
@pytest.fixture
def mock_db():
    with patch("openai_api_client.services.user.get_db") as mock_get_db:
        mock_session = MagicMock(spec=Session)
        mock_get_db.return_value = mock_session
        yield mock_session

# Test cases for user registration
class TestUserService_CreateUser:
    def test_create_user_success(self, mock_db):
        """Test successful user creation with valid data."""
        request = UserCreate(username="testuser", email="test@example.com", password="testpassword")
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        service = user_service(db=mock_db)
        user = service.create_user(request)
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.api_key is None
        mock_db.add.assert_called_once_with(User(username="testuser", email="test@example.com", password=pwd_context.hash("testpassword")))
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(User(username="testuser", email="test@example.com", password=pwd_context.hash("testpassword")))

    def test_create_user_username_exists(self, mock_db):
        """Test handling of duplicate username."""
        request = UserCreate(username="testuser", email="test@example.com", password="testpassword")
        mock_db.add.side_effect = IntegrityError(None, None, "users_username_key")
        mock_db.rollback.return_value = None
        service = user_service(db=mock_db)
        with pytest.raises(HTTPException) as exc:
            service.create_user(request)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Username already exists" in str(exc.value.detail)

    def test_create_user_email_exists(self, mock_db):
        """Test handling of duplicate email."""
        request = UserCreate(username="testuser", email="test@example.com", password="testpassword")
        mock_db.add.side_effect = IntegrityError(None, None, "users_email_key")
        mock_db.rollback.return_value = None
        service = user_service(db=mock_db)
        with pytest.raises(HTTPException) as exc:
            service.create_user(request)
        assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Email already exists" in str(exc.value.detail)

    def test_create_user_general_error(self, mock_db):
        """Test handling of general error during user creation."""
        request = UserCreate(username="testuser", email="test@example.com", password="testpassword")
        mock_db.add.side_effect = Exception("General error")
        mock_db.rollback.return_value = None
        service = user_service(db=mock_db)
        with pytest.raises(HTTPException) as exc:
            service.create_user(request)
        assert exc.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error creating user" in str(exc.value.detail)

# Test cases for user authentication
class TestUserService_AuthenticateUser:
    def test_authenticate_user_success(self, mock_db):
        """Test successful user authentication with valid credentials."""
        request = UserLogin(email="test@example.com", password="testpassword")
        mock_db.query.return_value.filter.return_value.first.return_value = User(id=1, username="testuser", email="test@example.com", password=pwd_context.hash("testpassword"))
        service = user_service(db=mock_db)
        user = service.authenticate_user(request)
        assert user.id == 1
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        mock_db.query.assert_called_once_with(User)
        mock_db.query(User).filter.assert_called_once_with(User.email == "test@example.com")
        mock_db.query(User).filter(User.email == "test@example.com").first.assert_called_once()

    def test_authenticate_user_invalid_credentials(self, mock_db):
        """Test handling of invalid email or password."""
        request = UserLogin(email="test@example.com", password="testpassword")
        mock_db.query.return_value.filter.return_value.first.return_value = None
        service = user_service(db=mock_db)
        with pytest.raises(HTTPException) as exc:
            service.authenticate_user(request)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in str(exc.value.detail)

    def test_authenticate_user_incorrect_password(self, mock_db):
        """Test handling of incorrect password."""
        request = UserLogin(email="test@example.com", password="wrongpassword")
        mock_db.query.return_value.filter.return_value.first.return_value = User(id=1, username="testuser", email="test@example.com", password=pwd_context.hash("testpassword"))
        service = user_service(db=mock_db)
        with pytest.raises(HTTPException) as exc:
            service.authenticate_user(request)
        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect password" in str(exc.value.detail)

# Test cases for retrieving user by ID
class TestUserService_GetUserById:
    def test_get_user_by_id_success(self, mock_db):
        """Test successful retrieval of a user by ID."""
        user_id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = User(id=user_id, username="testuser", email="test@example.com", password=pwd_context.hash("testpassword"))
        service = user_service(db=mock_db)
        user = service.get_user_by_id(user_id)
        assert user.id == user_id
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        mock_db.query.assert_called_once_with(User)
        mock_db.query(User).filter.assert_called_once_with(User.id == user_id)
        mock_db.query(User).filter(User.id == user_id).first.assert_called_once()

    def test_get_user_by_id_not_found(self, mock_db):
        """Test handling of user not found."""
        user_id = 1
        mock_db.query.return_value.filter.return_value.first.return_value = None
        service = user_service(db=mock_db)
        with pytest.raises(HTTPException) as exc:
            service.get_user_by_id(user_id)
        assert exc.value.status_code == status.HTTP_404_NOT_FOUND
        assert "User not found" in str(exc.value.detail)

# Test cases for generating JWT access token
class TestCreateAccessToken:
    def test_create_access_token(self):
        """Test generating a JWT access token with valid user data."""
        user_id = 1
        data = {"sub": user_id}
        token = create_access_token(data)
        # Verify the token structure and content
        assert isinstance(token, str) 
        # (Add specific assertions based on your JWT token structure)

# Test cases for verifying JWT access token
class TestVerifyAccessToken:
    # (Add test cases for `verify_access_token` function, similar to the above test cases)

# Test cases for retrieving the current user
class TestGetCurrentUser:
    # (Add test cases for `get_current_user` function, similar to the above test cases)