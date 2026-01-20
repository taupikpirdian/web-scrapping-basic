"""Market scraper service module."""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.models.config import BASE_WEB
from src.models.market_data import MarketData
from src.scraper.fetcher import fetch_page
from src.parsers.html_parser import (
    extract_current_price,
    extract_last_update,
    extract_price_details,
)


def scrape_market(emiten: str) -> MarketData:
    """Scrape data market dari Katadata untuk emiten tertentu.

    Args:
        emiten: Kode saham emiten (contoh: 'BBCA', 'INDF')

    Returns:
        MarketData object berisi data market harga saham
    """
    url = f"{BASE_WEB}/{emiten.lower()}"
    soup = fetch_page(url)

    current_price = extract_current_price(soup)
    price_details = extract_price_details(soup)
    last_update = extract_last_update(soup)

    return MarketData(
        emiten=emiten.upper(),
        url=url,
        date_time_scraping=datetime.now(
            ZoneInfo("Asia/Jakarta")
        ).isoformat(),
        price=current_price,
        high_price=price_details["high"],
        low_price=price_details["low"],
        last_price=price_details["last"],
        open_price=price_details["open"],
        last_update_text=(
            last_update.strftime("%Y-%m-%d %H:%M:%S")
            if last_update
            else None
        )
    )
