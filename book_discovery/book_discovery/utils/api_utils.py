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
