import pytest
from config import TestConfig
from book_discovery.db import db
from app import create_app  # Ensure 'app.py' is in the project root (not inside a package)

@pytest.fixture(scope="session")
def app():
    """Creates a Flask app with test config."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Provides a test client for HTTP request tests."""
    return app.test_client()

@pytest.fixture
def session(app):
    """Provides a scoped SQLAlchemy session for direct DB access in tests."""
    with app.app_context():
        yield db.session

@pytest.fixture(autouse=True)
def clean_db(session):
    """Rollback any changes after each test to prevent cross-test pollution."""
    yield
    session.rollback()

