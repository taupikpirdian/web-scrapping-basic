"""HTML parsing utilities."""

import re
from datetime import datetime
from typing import Dict, Optional
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup

from src.parsers.number_parser import parse_id_number


def extract_current_price(soup: BeautifulSoup) -> Optional[float]:
    """Ekstrak harga saat ini dari halaman.

    Args:
        soup: BeautifulSoup object

    Returns:
        Harga saat ini sebagai float, atau None jika tidak ditemukan
    """
    current_price_el = soup.select_one("h1.currentprice")
    if current_price_el:
        return parse_id_number(current_price_el.text.strip())
    return None


def extract_price_details(soup: BeautifulSoup) -> Dict[str, Optional[float]]:
    """Ekstrak detail harga (high, low, last, open) dari halaman.

    Args:
        soup: BeautifulSoup object

    Returns:
        Dictionary dengan keys: high, low, last, open
    """
    rows = soup.select(".marketprice .row .col-3")
    price_details = {
        "high": None,
        "low": None,
        "last": None,
        "open": None
    }

    for col in rows:
        label = col.find("p")
        value = col.find_all("p")[-1]

        if not label or not value:
            continue

        label_text = label.text.strip().lower()
        price_value = parse_id_number(value.text.strip())

        if label_text in price_details:
            price_details[label_text] = price_value

    return price_details


def extract_last_update(soup: BeautifulSoup) -> Optional[datetime]:
    """Ekstrak dan parse datetime dari elemen last-update.

    Args:
        soup: BeautifulSoup object

    Returns:
        datetime object dengan timezone Asia/Jakarta, atau None
    """
    update_el = soup.select_one(".last-update")
    if not update_el:
        return None

    last_update = update_el.get_text(" ", strip=True)
    match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", last_update)

    if match:
        return datetime.strptime(
            match.group(1),
            "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=ZoneInfo("Asia/Jakarta"))
    return None
