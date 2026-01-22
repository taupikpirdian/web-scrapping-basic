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
│   │   ├── market_data.py     # Model data market
│   │   └── database.py        # Database functions
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
├── migrations/                # Database migrations
│   ├── README.md
│   ├── run_migration.py       # Script untuk menjalankan migration
│   ├── 001_create_market_data_table.sql       # PostgreSQL migration
│   ├── 001_create_market_data_table_mysql.sql # MySQL migration
│   └── 001_rollback_market_data_table.sql     # Rollback migration
├── tests/                     # Unit tests
│   └── __init__.py
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env.example               # Contoh environment variables
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

3. Jika ingin menyimpan ke database, install tambahan dependencies:

Untuk MySQL (Primary):
```bash
pip install mysql-connector-python
```

Untuk PostgreSQL:
```bash
pip install psycopg2-binary
```

## Usage

### Scrape ke JSON

Konfigurasi daftar emiten yang ingin di-scrape melalui file `.env` (variable `EMITEN_LIST`).

```bash
# Jalankan scraper
python main.py
```

Output akan disimpan di `market_data.json`.

### Scrape dan Simpan ke Database

1. Setup environment variables:
```bash
cp .env.example .env
# Edit .env sesuai konfigurasi database dan daftar emiten Anda
```

Contoh konfigurasi `.env`:
```env
EMITEN_LIST=bbca,indf,tlkm,unvr
DB_TYPE=mysql
DB_HOST=localhost
...
```

2. Jalankan database migration:
```bash
# MySQL (Primary)
python migrations/run_migration.py --database mysql --user root --db myorbit_market_data --password your_password

# PostgreSQL
python migrations/run_migration.py --database postgresql --user postgres --db market_data --password your_password
```

Atau gunakan perintah MySQL langsung:
```bash
mysql -u root -p myorbit_market_data < migrations/001_create_market_data_table_mysql.sql
```

3. Scrape dan simpan ke database:
```bash
python main.py --save-db
```

### Contoh Query Database

```sql
-- Ambil data terbaru per emiten
SELECT * FROM v_latest_market_data ORDER BY emiten;

-- Ambil 10 data terakhir untuk BBCA
SELECT * FROM market_data
WHERE emiten = 'BBCA'
ORDER BY date_time_scraping DESC
LIMIT 10;

-- Ambil data berdasarkan date range
SELECT * FROM market_data
WHERE date_time_scraping >= '2025-01-01'
  AND date_time_scraping < '2025-02-01'
ORDER BY date_time_scraping DESC;
```

## Features

- Clean architecture dengan separation of concerns
- Mengikuti PEP 8 standards
- Type hints untuk better code quality
- Dataclass untuk model data
- Single Responsibility Principle (SRP)
- Mudah di-test dan di-maintain
- **NEW**: Database support (PostgreSQL/MySQL)
- **NEW**: Migration scripts
- **NEW**: Command-line arguments

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

### Menambah Emiten Baru

```bash
# Via command line
python main.py --emiten bbca indf tlkm
```

### Database Configuration

Set environment variables di `.env`:
```
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=myorbit_market_data
```

### Migration Rollback

```bash
# MySQL
python migrations/run_migration.py --database mysql --user root --db myorbit_market_data --password your_password --rollback

# Atau gunakan perintah MySQL langsung
mysql -u root -p myorbit_market_data < migrations/001_rollback_market_data_table_mysql.sql
```

## License

MIT
