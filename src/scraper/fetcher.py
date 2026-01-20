"""Web fetcher module."""

import requests
from bs4 import BeautifulSoup

from src.models.config import HEADERS


def fetch_page(url: str) -> BeautifulSoup:
    """Fetch halaman web dan return BeautifulSoup object.

    Args:
        url: URL yang akan di-fetch

    Returns:
        BeautifulSoup object yang berisi HTML content

    Raises:
        requests.HTTPError: Jika request gagal
    """
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")
