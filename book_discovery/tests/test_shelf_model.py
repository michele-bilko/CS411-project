import pytest
import uuid

from book_discovery.models.shelf_model import ShelfModel
from book_discovery.models.books_model import Books
from book_discovery.db import db

@pytest.fixture
def shelf():
    return ShelfModel()

@pytest.fixture
def book(session):
    """Create a unique test book for each test."""
    unique_id = f"book_{uuid.uuid4().hex[:8]}"
    book_data = {
        "google_books_id": unique_id,
        "title": "Shelf Test Book",
        "authors": "Jane Reader",
        "genres": "Sci-Fi",
        "description": "Testing shelf operations",
        "page_count": 456,
        "date_published": "2023",
        "rating": 4
    }
    Books.create_book(**book_data)
    return Books.get_book_by_google_books_id(unique_id)

def test_add_book_to_tbr(shelf, book):
    shelf.add_book_to_tbr(book.id)
    assert book.id in shelf.tbr

def test_add_book_to_tbr_duplicate(shelf, book):
    shelf.add_book_to_tbr(book.id)
    with pytest.raises(ValueError, match="already in tbr"):
        shelf.add_book_to_tbr(book.id)

def test_begin_reading(shelf, book):
    shelf.add_book_to_tbr(book.id)
    shelf.begin_reading(book.id)
    assert book.id in shelf.currently_reading
    assert book.id not in shelf.tbr

def test_finish_reading(shelf, book):
    shelf.add_book_to_tbr(book.id)
    shelf.begin_reading(book.id)
    shelf.finish_reading(book.id)
    assert book.id in shelf.finished_reads
    assert book.id not in shelf.currently_reading

def test_remove_book_from_list(shelf, book):
    shelf.add_book_to_tbr(book.id)
    shelf.remove_book_from_list(book.id, "tbr")
    assert book.id not in shelf.tbr

def test_assign_book_rating(shelf, book):
    shelf.add_book_to_tbr(book.id)
    shelf.assign_book_rating(book.id, 5)
    assert book.rating == 5

def test_get_tbr_books(shelf, book):
    shelf.add_book_to_tbr(book.id)
    books = shelf.get_tbr_books()
    assert any(b.id == book.id for b in books)

def test_clear_cache(shelf, book):
    shelf.add_book_to_tbr(book.id)
    assert book.id in shelf._book_cache
    shelf.clear_cache()
    assert shelf._book_cache == {}

