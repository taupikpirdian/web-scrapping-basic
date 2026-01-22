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

### Option 1: Docker (Recommended untuk Production)

Docker adalah cara yang disarankan untuk menjalankan scraper di production server. Tidak perlu install Python atau dependencies secara manual.

**Prasyarat:**
- Docker dan Docker Compose terinstall di server
- MySQL sudah berjalan di server

**Setup:**

1. Build dan jalankan container:
```bash
# Build image
docker build -t market-scraper .

# Atau gunakan docker-compose (lebih mudah)
docker-compose up
```

2. Jalankan dengan docker-compose:
```bash
# Jalankan scraper
docker-compose run --rm market-scraper

# Atau jalankan di background
docker-compose up -d
```

3. Setup cron job di server untuk menjalankan scraper secara berkala:
```bash
# Edit crontab
crontab -e

# Tambahkan salah satu dari opsi berikut:

# Opsi 1: Gunakan script run-scraper.sh (recommended)
*/30 * * * * /path/to/web-scrapping-basic/run-scraper.sh >> /var/log/market-scraper.log 2>&1

# Opsi 2: Jalankan setiap jam
0 * * * * cd /path/to/web-scrapping-basic && /usr/local/bin/docker-compose run --rm market-scraper

# Opsi 3: Setiap 30 menit
*/30 * * * * cd /path/to/web-scrapping-basic && /usr/local/bin/docker-compose run --rm market-scraper

# Opsi 4: Setiap hari jam 08:00 dan 16:00
0 8,16 * * * cd /path/to/web-scrapping-basic && /usr/local/bin/docker-compose run --rm market-scraper
```

**Tips Cron:**
- `>> /var/log/market-scraper.log 2>&1` akan menyimpan output ke log file
- Cek log dengan: `tail -f /var/log/market-scraper.log`
- Cek cron job yang aktif dengan: `crontab -l`

### Option 2: Python Virtual Environment (Untuk Development)

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

### Dengan Docker

1. Setup environment variables:
```bash
cp .env.example .env
# Edit .env sesuai konfigurasi database MySQL Anda
```

Contoh `.env` untuk Docker:
```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=myorbit_market_data
EMITEN_LIST=bbca,indf,tlkm,unvr
```

2. Jalankan database migration:

**Opsi 1: Menggunakan helper script (paling mudah)**
```bash
# Script akan otomatis baca konfigurasi dari .env
./run-migration.sh
```

**Opsi 2: Menggunakan Python script**
```bash
# Menggunakan script Python dengan parameter
python migrations/run_migration.py --database mysql --user root --db myorbit_market_data --password your_password

# Atau gunakan env var untuk password
export DB_PASSWORD=your_password
python migrations/run_migration.py --database mysql --user root --db myorbit_market_data
```

**Opsi 3: Menggunakan MySQL command langsung**
```bash
mysql -u root -p myorbit_market_data < migrations/001_create_market_data_table_mysql.sql
```

3. Jalankan scraper:
```bash
# Jalankan sekali
docker-compose run --rm market-scraper

# Atau dengan docker command langsung
docker run --rm \
  --network host \
  -e DB_HOST=localhost \
  -e DB_USER=root \
  -e DB_PASSWORD=your_password \
  -e DB_NAME=myorbit_market_data \
  -e EMITEN_LIST=bbca,indf \
  market-scraper
```

### Tanpa Docker (Development)

#### Scrape ke JSON

Konfigurasi daftar emiten yang ingin di-scrape melalui file `.env` (variable `EMITEN_LIST`).

```bash
# Aktifkan virtual environment
source venv/bin/activate

# Jalankan scraper
python main.py
```

Output akan disimpan di `market_data.json`.

#### Scrape dan Simpan ke Database

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

## Deployment dengan Docker

### Keuntungan Menggunakan Docker

✓ **Tidak perlu install Python** di server - semua dependencies sudah dibungkus dalam Docker image
✓ **Environment yang konsisten** - development dan production menggunakan environment yang sama
✓ **Isolasi** - scraper tidak mengganggu aplikasi lain di server
✓ **Easy rollback** - bisa dengan mudah kembali ke versi sebelumnya
✓ **Scalable** - mudah untuk scaling jika diperlukan

### Langkah Deployment di Server

1. **Upload code ke server:**
```bash
scp -r /path/to/web-scrapping-basic user@server:/opt/
```

2. **Setup database:**
```bash
# Login ke server
ssh user@server

# Buat database
mysql -u root -p
CREATE DATABASE myorbit_market_data;

# Jalankan migration
cd /opt/web-scrapping-basic

# Opsi 1: Menggunakan Python script (recommended)
python migrations/run_migration.py --database mysql --user root --db myorbit_market_data --password your_password

# Opsi 2: Menggunakan MySQL command
mysql -u root -p myorbit_market_data < migrations/001_create_market_data_table_mysql.sql
```

3. **Setup environment:**
```bash
cd /opt/web-scrapping-basic
cp .env.example .env
nano .env  # Edit sesuai konfigurasi
```

4. **Build Docker image:**
```bash
docker-compose build
```

5. **Test run:**
```bash
docker-compose run --rm market-scraper
```

6. **Setup cron:**
```bash
crontab -e
# Tambahkan:
*/30 * * * * /opt/web-scrapping-basic/run-scraper.sh >> /var/log/market-scraper.log 2>&1
```

7. **Monitoring:**
```bash
# Cek log
tail -f /var/log/market-scraper.log

# Cek apakah cron jalan
grep CRON /var/log/syslog

# Cek data di database
mysql -u root -p -e "SELECT * FROM myorbit_market_data.market_data ORDER BY date_time_scraping DESC LIMIT 10;"
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
