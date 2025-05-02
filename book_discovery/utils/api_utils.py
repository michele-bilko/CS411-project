import logging
import os
import requests
from dotenv import load_dotenv

from book_discovery.utils.logger import configure_logger

load_dotenv()

logger = logging.getLogger(__name__)
configure_logger(logger)


GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

def search_books(query: str) -> dict:
	"""Search a for a book based on a querey"""

	params = {"q": query,"key": API_KEY,}
	try:
		response = requests.get(GOOGLE_BOOKS_API_URL, params=params)
		response.raise_for_status()
		return response.json()
		
	except requests.exceptions.RequestException as e:
		raise RuntimeError(f"Request to Google books failed failed: {e}")

def get_book_details(book_id: str) -> dict:
	"""Retrieve information for a specific book using its Google Books ID"""
	try:
		response = requests.get(f"{GOOGLE_BOOKS_API_URL}/{book_id}", params={"key": API_KEY})
		response.raise_for_status()
		return response.json()
	
	except requests.exceptions.RequestException as e:
		raise RuntimeError(f"Error retrieving details for book ID '{book_id}': {e}")
RANDOM_ORG_URL = os.getenv("RANDOM_ORG_URL",
    "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new")

def get_random() -> float:
    """
    Fetches a random float between 0 and 1 from random.org.
    """
    try:
        response = requests.get(RANDOM_ORG_URL, timeout=5)
        response.raise_for_status()
        return float(response.text.strip())
    except ValueError:
        raise ValueError(f"Invalid response from random.org: {response.text}")
    except requests.exceptions.Timeout:
        raise RuntimeError("Request to random.org timed out.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request to random.org failed: {e}")
