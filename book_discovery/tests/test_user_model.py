import pytest
import uuid
from book_discovery.models.user_model import Users
from book_discovery.db import db

@pytest.fixture
def sample_user_data():
    """Generate a unique test user each time to avoid duplicate conflicts."""
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    return {
        "username": unique_username,
        "password": "securepass123"
    }

def test_create_user(session, sample_user_data):
    Users.create_user(**sample_user_data)
    user_id = Users.get_id_by_username(sample_user_data["username"])
    assert isinstance(user_id, int)

def test_duplicate_user_creation(session, sample_user_data):
    Users.create_user(**sample_user_data)
    with pytest.raises(ValueError, match="already exists"):
        Users.create_user(**sample_user_data)

def test_check_password_success(session, sample_user_data):
    Users.create_user(**sample_user_data)
    assert Users.check_password(sample_user_data["username"], "securepass123") is True

def test_check_password_failure(session, sample_user_data):
    Users.create_user(**sample_user_data)
    assert Users.check_password(sample_user_data["username"], "wrongpass") is False

def test_delete_user(session, sample_user_data):
    Users.create_user(**sample_user_data)
    Users.delete_user(sample_user_data["username"])
    with pytest.raises(ValueError):
        Users.check_password(sample_user_data["username"], "securepass123")

def test_update_password(session, sample_user_data):
    Users.create_user(**sample_user_data)
    Users.update_password(sample_user_data["username"], "newpassword456")
    assert Users.check_password(sample_user_data["username"], "newpassword456") is True

