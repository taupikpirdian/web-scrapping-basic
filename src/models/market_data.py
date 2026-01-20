"""Data models for market information."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class MarketData:
    """Model untuk data market harga saham.

    Attributes:
        emiten: Kode saham emiten
        url: URL sumber data
        date_time_scraping: Waktu scraping dilakukan
        price: Harga saat ini
        high_price: Harga tertinggi
        low_price: Harga terendah
        last_price: Harga terakhir
        open_price: Harga pembukaan
        last_update_text: Text waktu update terakhir
    """

    emiten: str
    url: str
    date_time_scraping: str
    price: Optional[float]
    high_price: Optional[float]
    low_price: Optional[float]
    last_price: Optional[float]
    open_price: Optional[float]
    last_update_text: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert model ke dictionary.

        Returns:
            Dictionary representation dari market data
        """
        return {
            "emiten": self.emiten,
            "url": self.url,
            "date_time_scraping": self.date_time_scraping,
            "data": {
                "price": self.price,
                "high_price": self.high_price,
                "low_price": self.low_price,
                "last_price": self.last_price,
                "open_price": self.open_price,
                "last_update_text": self.last_update_text,
            }
        }
