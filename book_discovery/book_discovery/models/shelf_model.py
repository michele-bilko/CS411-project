import logging
import math
import os
import time
from typing import List, Dict

from book_discovery.models.books_model import Books
from book_discovery.utils.logger import configure_logger
from book_discovery.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class ShelfModel:
    """A class to manage an individual user's reading activity.
    """

    def __init__(self):
        """Initializes the ShelfModel with 3 initially empty lists: tbr, currently_reading, finished_reads.

        The shelf is initially empty, and the book cache and time-to-live (TTL) caches are also initialized.
        The TTL is set to 60 seconds by default, but this can be overridden by setting the TTL_SECONDS environment variable.

        Attributes:
            tbr (List[str]): A list with to-read books.
            currently_reading (List[str]): A list of in-progress reads.
            finished_reads: A list of completed reads.
            _book_cache (dict[int, Books]): A cache to store book objects for quick access.
            _ttl (dict[int, float]): A cache to store the time-to-live for each boxer.
            ttl_seconds (int): The time-to-live in seconds for the cached boxer objects.

        """

        self.tbr: List[str] = []
        self.currently_reading: List[str] = []
        self.finished_reads: List[str] = []
        self._book_cache: dict[int, Books] = {}
        self._ttl: dict[int, float] = {}
        self.ttl_seconds = int(os.getenv("TTL_SECONDS", 60))


    def add_book_to_tbr(self, book_id: str):
        """Add a new book to the tbr list.

        Args:
            book_id (str): The ID of the book to be added to the tbr list.

        Raises:
            ValueError: If the book ID is invalid or the book does not exist.

        """

        if book_id in self.tbr:
            logger.warning(f"Book ID {book_id} is already in tbr list.")
            raise ValueError("Book already in tbr list.")
        
        now = time.time()

        if book_id in self._book_cache and self._ttl.get(book_id, 0) > now:
                logger.debug(f"Book ID {book_id} retrieved from cache")
                book = self._book_cache[book_id]
        else:
            try:
                book = Books.get_book_by_id(book_id)
                logger.info(f"Book ID {book_id} loaded from DB")

            except ValueError as e:
                logger.error(str(e))
                raise

        self._book_cache[book_id] = book
        self._ttl[book_id] = now + self.ttl_seconds

        logger.info(f"Adding book '{book.title}' (ID {book_id}) to the tbr list.")

        self.tbr.append(book_id)

        
    def begin_reading(self, book_id: str):
        """Begin reading a new book by moving it from the tbr list to the currently_reading list.

        Args:
            book_id (str): The ID of the book to be added to the currently_reading list.

        Raises:
            ValueError: If the book ID is invalid or the book does not exist.

        """

        if book_id not in self.tbr:
            logger.warning(f"Book ID {book_id} must be added to tbr before it can be moved to current reads.")
            raise ValueError("Book ID {book_id} must be added to tbr before it can be moved to current reads.")
        
        if book_id in self.currently_reading:
            logger.warning(f"Book ID {book_id} is already in currently_reading list.")
            raise ValueError("Book already in currently_reading list.")
        
        now = time.time()

        if book_id in self._book_cache and self._ttl.get(book_id, 0) > now:
                logger.debug(f"Book ID {book_id} retrieved from cache")
                book = self._book_cache[book_id]
        else:
            try:
                book = Books.get_book_by_id(book_id)
                logger.info(f"Book ID {book_id} loaded from DB")

            except ValueError as e:
                logger.error(str(e))
                raise

        self._book_cache[book_id] = book
        self._ttl[book_id] = now + self.ttl_seconds

        logger.info(f"Moving book '{book.title}' (ID {book_id}) to the currently_reading list.")

        self.tbr.remove(book_id)
        self.currently_reading.append(book_id)


        
    def finish_reading(self, book_id: str):
        """Mark a book as finished by moving it from the currently_reading list to the finished_reads list.

        Args:
            book_id (str): The ID of the book to be added to the finished_reads list.

        Raises:
            ValueError: If the book ID is invalid or the book does not exist.

        """

        if book_id not in self.currently_reading:
            logger.warning(f"Book ID {book_id} must already be in currently_reading in order to mark it as finished.")
            raise ValueError("Book ID {book_id} must already be in currently_reading in order to mark it as fini\
shed.")

        if book_id in self.tbr:
            logger.warning(f"Book ID {book_id} is already in finished_reads list.")
            raise ValueError("Book already in finished_reads_list.")
        
        now = time.time()

        if book_id in self._book_cache and self._ttl.get(book_id, 0) > now:
                logger.debug(f"Book ID {book_id} retrieved from cache")
                book = self._book_cache[book_id]
        else:
            try:
                book = Books.get_book_by_id(book_id)
                logger.info(f"Book ID {book_id} loaded from DB")

            except ValueError as e:
                logger.error(str(e))
                raise

        self._book_cache[book_id] = book
        self._ttl[book_id] = now + self.ttl_seconds

        logger.info(f"Adding book '{book.title}' (ID {book_id}) to the finished_reads list.")

        self.currently_reading.remove(book_id)
        self.finished_reads.append(book_id)


    def remove_book_from_list(self, book_id: str, book_list: str):
        """
        Remove book from the specified list.
        
        Args:
            book_id (str): The Google Books ID of the book to remove.
            book_list (str): The appropriate list from which to remove the book.

        Raises:
            ValueError: If the book is not contained in the specified list or the list name is not valid.
        
        """
        logger.info(f"Removing book {book_id} from {book_list}")

        if book_list == "tbr":
            if book_id not in self.tbr:
                logger.warning(f"Book ID {book_id} is not on the specified list.")
                raise ValueError("Book ID {book_id} is not on the specified list.")
            self.tbr.remove(book_id)
            

        elif book_list == "currently_reading":
            if book_id not in self.currently_reading:
                logger.warning(f"Book ID {book_id} is not on the specified list.")
                raise ValueError("Book ID {book_id} is not on the specified list.")
            self.currently_reading.remove(book_id)

        elif book_list == "finished_reads":
            if book_id not in self.finished_reads:
                logger.warning(f"Book ID {book_id} is not on the specified list.")
                raise ValueError("Book ID {book_id} is not on the specified list.")
            self.finished_reads.remove(book_id)

        else:
            logger.error(f"Invalid book list: {book_list}.")
            ValueError(f"Invalid book list: {book_list}.")
    
            
        


    def get_boxers(self) -> List[Boxers]:
        """Retrieves the current list of boxers in the ring.

        Returns:
            List[Boxers]: A list of Boxers dataclass instances representing the boxers in the ring.

        """
        if not self.ring:
            logger.warning("Retrieving boxers from an empty ring.")
            return []
        else:
            logger.info(f"Retrieving {len(self.ring)} boxers from the ring.")

        now = time.time()
        boxers = []
        
        for boxer_id in self.ring:
            if boxer_id not in self._boxer_cache or self._ttl.get(boxer_id, 0) < now:
                logger.info(f"TTL expired or missing for boxer {boxer_id}. Refreshing from DB.")
                boxer = Boxers.get_boxer_by_id(boxer_id)
                self._boxer_cache[boxer_id] = boxer
                self._ttl[boxer_id] = now + self.ttl_seconds
            else:
                logger.debug(f"Using cached boxer {boxer_id} (TTL valid).")

            boxers.append(self._boxer_cache[boxer_id])

        logger.info(f"Retrieved {len(boxers)} boxers from the ring.")
        return boxers

    def clear_cache(self):
        """Clears the local TTL cache of book objects.

        """
        logger.info("Clearing local books cache in ShelfModel.")
        self._book_cache.clear()
        self._ttl.clear()
