# Market Data Scraper

Web scraper untuk mengambil data market saham dari Katadata.

## Project Structure

```
web-scrapping-basic/
├── src/
│   ├── __init__.py
│   ├── models/                 # Data models dan configuration
│   │   ├── __init__.py
│   │   ├── config.py          # Konstanta konfigurasi
│   │   └── market_data.py     # Model data market
│   ├── scraper/               # Web fetching module
│   │   ├── __init__.py
│   │   └── fetcher.py         # HTTP fetcher
│   ├── parsers/               # HTML dan number parsing
│   │   ├── __init__.py
│   │   ├── html_parser.py     # Parser HTML
│   │   └── number_parser.py   # Parser angka Indonesia
│   └── services/              # Business logic
│       ├── __init__.py
│       └── market_scraper.py  # Service untuk scrape market
├── tests/                     # Unit tests
│   └── __init__.py
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .gitignore
└── README.md
```

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python main.py
```

Output akan disimpan di `market_data.json`.

## Features

- Clean architecture dengan separation of concerns
- Mengikuti PEP 8 standards
- Type hints untuk better code quality
- Dataclass untuk model data
- Single Responsibility Principle (SRP)
- Mudah di-test dan di-maintain

## Example Output

```json
[
  {
    "emiten": "BBCA",
    "url": "https://databoks.katadata.co.id/marketdata/bbca",
    "date_time_scraping": "2025-01-21T10:30:00+07:00",
    "data": {
      "price": 9200.0,
      "high_price": 9250.0,
      "low_price": 9150.0,
      "last_price": 9200.0,
      "open_price": 9180.0,
      "last_update_text": "2025-01-21 10:28:45"
    }
  }
]
```

## Development

Untuk menambahkan emiten baru, edit `main.py`:
```python
emiten_list = [
    "bbca",
    "indf",
    "tlkm"  # tambahkan emiten baru di sini
]
```

## License

MIT
