import pytest
import requests
from book_discovery.utils.api_utils import search_books, get_book_details

MOCK_QUERY = "python"
MOCK_BOOK_ID = "abc123"

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch("requests.get")

def test_search_books_success(mock_requests_get):
    mock_response = mock_requests_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"items": [{"title": "Python 101"}]}

    result = search_books(MOCK_QUERY)
    assert "items" in result
    assert result["items"][0]["title"] == "Python 101"

def test_search_books_failure(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.RequestException("fail")
    with pytest.raises(RuntimeError, match="Request to Google books failed"):
        search_books(MOCK_QUERY)

def test_get_book_details_success(mock_requests_get):
    mock_response = mock_requests_get.return_value
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"id": MOCK_BOOK_ID, "title": "Sample"}

    result = get_book_details(MOCK_BOOK_ID)
    assert result["id"] == MOCK_BOOK_ID
    assert result["title"] == "Sample"

def test_get_book_details_failure(mock_requests_get):
    mock_requests_get.side_effect = requests.exceptions.RequestException("bad req")
    with pytest.raises(RuntimeError, match=f"Error retrieving details for book ID '{MOCK_BOOK_ID}'"):
        get_book_details(MOCK_BOOK_ID)

