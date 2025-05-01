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



    def __init__(self, google_books_id, title, authors, genres=None, description=None, page_count=None, date_published=None):
        """Initialize a new Book instance with basic attributes.

        Args:
            google_books_id (str): Unique Google Books Identifier.
            title (str): Title of the book.
            authors (str): Author(s) of the book.
            genres (str): genre(s) or categories of the book.
            description (str): A brief description of the book.
            page_count (int): The book's page count.
            date_published (str): The book's date or year of publication.

        """

        self.google_books_id = google_books_id
        self.title = title
        self.authors = authors
        self.genres = genres
        self.description = description
        self.page_count = page_count
        self.date_published = date_published

        

    @classmethod
    def create_book(cls, google_books_id: str, title: str, authors: str, genres: str = None, description: str = None, page_count: int = None, date_published: str = None) -> None:
        """Create and persist a new Book.

        Args:
            google_books_id: Unique Google Books Identifier.
            title: Title of the book.
            authors: Author(s) of the book.
            genres: genre(s) or categories of the book.
            description: A brief description of the book.
            page_count: The book's page count.
            date_published: The book's date or year of publication.

        Raises:
            ValueError: If a book with the same name already exists.
            SQLAlchemyError: If there is a database error during creation.

        """
        logger.info(f"Creating boxer: {name}, {weight=} {height=} {reach=} {age=}")

        
        try:
            book = Books(google_books_id, title, authors, genres, description, page_count, date_published)

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
        """Retrieve a boxer by ID.

        Args:
            boxer_id: The ID of the boxer.

        Returns:
            Boxer: The boxer instance.

        Raises:
            ValueError: If the boxer with the given ID does not exist.

        """

        logger.info(f"Attempting to retrieve boxer with ID {boxer_id}")

        
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
        """Retrieve a boxer by name.

        Args:
            name: The name of the boxer.

        Returns:
            Boxer: The boxer instance.

        Raises:
            ValueError: If the boxer with the given name does not exist.

        """
        logger.info(f"Attempting to retrieve boxer with name {name}")

        
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
    def delete(cls, boxer_id: int) -> None:
        """Delete a boxer by ID.

        Args:
            boxer_id: The ID of the boxer to delete.

        Raises:
            ValueError: If the boxer with the given ID does not exist.

        """
        boxer = cls.get_boxer_by_id(boxer_id)
        if boxer is None:
            logger.info(f"Boxer with ID {boxer_id} not found.")
            raise ValueError(f"Boxer with ID {boxer_id} not found.")
        db.session.delete(boxer)
        db.session.commit()
        logger.info(f"Boxer with ID {boxer_id} permanently deleted.")

    def update_stats(self, result: str) -> None:
        """Update the boxer's fight and win count based on result.

        Args:
            result: The result of the fight ('win' or 'loss').

        Raises:
            ValueError: If the result is not 'win' or 'loss'.
            ValueError: If the number of wins exceeds the number of fights.

        """
        if result not in {"win", "loss"}:
            raise ValueError("Result must be 'win' or 'loss'.")

        self.fights += 1
        if result == "win":
            self.wins += 1
        else:
            self.losses += 1  # Track losses for completeness

        if self.wins > self.fights:
            raise ValueError("Wins cannot exceed number of fights.")

        db.session.commit()
        logger.info(f"Updated stats for boxer {self.name}: {self.fights} fights, {self.wins} wins, {self.losses} losses")
    @staticmethod
    def get_leaderboard(sort_by: str = "wins") -> List[dict]:
        """Retrieve a sorted leaderboard of boxers.

        Args:
            sort_by (str): Either "wins" or "win_pct".

        Returns:
            List[Dict]: List of boxers with stats and win percentage.

        Raises:
            ValueError: If the sort_by parameter is not valid.

        """
        logger.info(f"Retrieving leaderboard. Sort by: {sort_by}")

        if sort_by not in {"wins", "win_pct"}:
            logger.error(f"Invalid sort_by parameter: {sort_by}")
            raise ValueError(f"Invalid sort_by parameter: {sort_by}")

        boxers = Boxers.query.filter(Boxers.fights > 0).all()

        def compute_win_pct(b: Boxers) -> float:
            return round((b.wins / b.fights) * 100, 1) if b.fights > 0 else 0.0

        leaderboard = [{
            "id": b.id,
            "name": b.name,
            "weight": b.weight,
            "height": b.height,
            "reach": b.reach,
            "age": b.age,
            "weight_class": b.weight_class,
            "fights": b.fights,
            "wins": b.wins,
            "win_pct": compute_win_pct(b)
        } for b in boxers]

        leaderboard.sort(key=lambda b: b[sort_by], reverse=True)
        logger.info("Leaderboard retrieved successfully.")
        return leaderboard
