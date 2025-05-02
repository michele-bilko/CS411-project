import pytest
import uuid
from book_discovery.models.books_model import Books
from book_discovery.db import db

@pytest.fixture
def sample_book_data():
    """Generate unique book data for each test to avoid duplication errors."""
    unique_id = f"book_{uuid.uuid4().hex[:8]}"
    return {
        "google_books_id": unique_id,
        "title": "Test Book",
        "authors": "John Doe",
        "genres": "Fiction",
        "description": "A sample test book",
        "page_count": 123,
        "date_published": "2020",
        "rating": 5
    }

def test_create_book(session, sample_book_data):
    Books.create_book(**sample_book_data)
    book = Books.get_book_by_google_books_id(sample_book_data["google_books_id"])
    assert book.title == "Test Book"
    assert book.authors == "John Doe"

def test_get_book_by_id_raises(session):
    with pytest.raises(ValueError, match="Book with ID 999 not found."):
        Books.get_book_by_id(999)

def test_delete_book(session, sample_book_data):
    Books.create_book(**sample_book_data)
    book = Books.get_book_by_google_books_id(sample_book_data["google_books_id"])
    Books.delete(book.id)
    with pytest.raises(ValueError):
        Books.get_book_by_id(book.id)

