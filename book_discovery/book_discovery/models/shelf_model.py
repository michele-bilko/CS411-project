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
            ValueError: If the boxer ID is invalid or the boxer does not exist.

        """
        
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

        logger.info(f"Adding book '{book.title}' (ID {book_id}) to the tbr")

        self.ring.append(book_id)


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

    def get_fighting_skill(self, boxer: Boxers) -> float:
        """Calculates the fighting skill for a boxer based on arbitrary rules.

        The fighting skill is computed as:
        - Multiply the boxer's weight by the number of letters in their name.
        - Subtract an age modifier (if age < 25, subtract 1; if age > 35, subtract 2).
        - Add a reach bonus (reach / 10).

        Args:
            boxer (Boxers): A Boxers dataclass representing the combatant.

        Returns:
            float: The calculated fighting skill.

        """
        logger.info(f"Calculating fighting skill for {boxer.name}: weight={boxer.weight}, age={boxer.age}, reach={boxer.reach}")

        # Arbitrary calculations
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        logger.info(f"Fighting skill for {boxer.name}: {skill:.3f}")
        return skill

    def clear_cache(self):
        """Clears the local TTL cache of boxer objects.

        """
        logger.info("Clearing local boxer cache in RingModel.")
        self._boxer_cache.clear()
        self._ttl.clear()
