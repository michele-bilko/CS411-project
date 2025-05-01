import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from book_discovery.db import db
from book_discovery.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class Books(db.Model):
    """Represents a book retrieved from Google Books API in the system.

    This model maps to the 'books' table in the database and stores metadata such as title, author, and publication info. Used in a Flask-SQLAlchemy application to allow users to discover, track, and manage books they're interested in reading.

    """
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    google_books_id = db.Column(db.String(40), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    genres = db.Column(db.String(100))
    description = db.Column(db.Text)
    page_count = db.Column(db.Integer)
    date_published = db.Column(db.String(20))
    rating = db.Column(db.Integer)



    def __init__(self, google_books_id, title, authors, genres=None, description=None, page_count=None, date_published=None, rating=None):
        """Initialize a new Book instance with basic attributes.

        Args:
            google_books_id (str): Unique Google Books Identifier.
            title (str): Title of the book.
            authors (str): Author(s) of the book.
            genres (str): genre(s) or categories of the book.
            description (str): A brief description of the book.
            page_count (int): The book's page count.
            date_published (str): The book's date or year of publication.
            rating (int): User-assigned rating from 1-5.

        """

        self.google_books_id = google_books_id
        self.title = title
        self.authors = authors
        self.genres = genres
        self.description = description
        self.page_count = page_count
        self.date_published = date_published

        

    @classmethod
    def create_book(cls, google_books_id: str, title: str, authors: str, genres: str = None, description: str = None, page_count: int = None, date_published: str = None, rating: int = None) -> None:
        """Create and persist a new Book.

        Args:
            google_books_id: Unique Google Books Identifier.
            title: Title of the book.
            authors: Author(s) of the book.
            genres: genre(s) or categories of the book.
            description: A brief description of the book.
            page_count: The book's page count.
            date_published: The book's date or year of publication.
            rating: User-assigned rating from 1-5.

        Raises:
            ValueError: If a book with the same name already exists.
            SQLAlchemyError: If there is a database error during creation.

        """
        logger.info(f"Creating book: {google_books_id}, {title}")

        
        try:
            book = Books(google_books_id, title, authors, genres, description, page_count, date_published, rating)

            existing = Books.query.filter_by(google_books_id=google_books_id).first()
            if existing:
                logger.error(f"Book: '{google_books_id}' already exists.")
                raise ValueError(f"Book with name '{google_books_id}' already exists.")

            db.session.add(book)
            db.session.commit()
            logger.info(f"Book '{title}' created successfully")
            
        except IntegrityError:
            logger.error(f"Book with ID '{google_books_id}' already exists in database.")
            db.session.rollback()
            raise ValueError(f"Book already exists in database.")
        
        except SQLAlchemyError as e:
            logger.error(f"Database error during creation: {e}")
            db.session.rollback()
            raise

    @classmethod
    def get_book_by_id(cls, book_id: int) -> "Books":
        """Retrieve a book by ID.

        Args:
            book_id: The ID of the book.

        Returns:
            Book: The book instance.

        Raises:
            ValueError: If the book with the given ID does not exist.

        """

        logger.info(f"Attempting to retrieve book with ID {book_id}")

        
        try:
            book = cls.query.get(book_id)
            
            if book is None:
                logger.info(f"Book with ID {book_id} not found.")
                raise ValueError(f"Book with ID {book_id} not found.")

            logger.info(f"Successfully retrieved book by ID: {book_id}")
            return book

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving book by ID {book_id}: {e}")
            raise
    

    @classmethod
    def get_book_by_google_books_id(cls, google_books_id: str) -> "Books":
        """Retrieve a book by its Google Books ID.

        Args:
            google_books_id: the Google Books ID for the book.

        Returns:
            Book: The book instance.

        Raises:
            ValueError: If the book with the given Google Books ID does not exist.

        """
        logger.info(f"Attempting to retrieve book with Google Books ID {google_books_id}")

        
        try:
            book = cls.query.filter_by(google_books_id=google_books_id).first()
            
            if book is None:
                logger.info(f"Book with Google Books ID {google_books_id} not found.")
                raise ValueError(f"Book with Google Books ID {google_books_id} not found.")

            logger.info(f"Successfully retrieved book by Google Books ID: {google_books_id}")
            return book

        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving book by Google Books ID {google_books_id}: {e}")
            raise

    @classmethod
    def delete(cls, book_id: int) -> None:
        """Delete a book by ID.

        Args:
            book_id: The ID of the book to delete.

        Raises:
            ValueError: If the book with the given ID does not exist.

        """
        book = cls.get_book_by_id(book_id)
        if book is None:
            logger.info(f"Book with ID {book_id} not found.")
            raise ValueError(f"Book with ID {book_id} not found.")
        db.session.delete(book)
        db.session.commit()
        logger.info(f"Book with ID {book_id} permanently deleted.")

    @classmethod
    def get_book_list(cls) -> List["Books"]:
        """Retrieve a list of all books in database sorted alphabetically by title.

        Returns:
            List[Books]: Sorted list of books.

        """
        logger.info(f"Retrieving list of books ordered alphabetically by title")

        books = Books.query.order_by(Books.title.asc()).all()
    
        logger.info("Books list retrieved successfully.")
        return books
