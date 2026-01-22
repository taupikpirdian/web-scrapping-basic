# Database Migrations

Folder ini berisi file-file migration SQL untuk database.

## Struktur Tabel

### market_data
Tabel untuk menyimpan data hasil scraping harga saham dari Katadata.

**Kolom:**
- `id` - Primary key (auto-increment)
- `emiten` - Kode saham emiten (contoh: BBCA, INDF)
- `url` - URL sumber data scraping
- `date_time_scraping` - Waktu ketika scraping dilakukan
- `last_update_text` - Waktu update terakhir dari sumber data
- `price` - Harga saham saat ini
- `high_price` - Harga tertinggi
- `low_price` - Harga terendah
- `last_price` - Harga terakhir
- `open_price` - Harga pembukaan
- `created_at` - Waktu record dibuat di database
- `updated_at` - Waktu record terakhir diupdate

**Index:**
- `idx_market_data_emiten` - Index pada kolom emiten
- `idx_market_data_date_time_scraping` - Index pada kolom date_time_scraping (descending)
- `idx_market_data_emiten_date` - Composite index emiten dan date_time_scraping
- `idx_market_data_last_update` - Index pada kolom last_update_text (descending)

**View:**
- `v_latest_market_data` - View untuk mendapatkan data terbaru per emiten

## Cara Menggunakan

### MySQL/MariaDB

**Jalankan Migration:**
```bash
mysql -u username -p database_name < migrations/001_create_market_data_table_mysql.sql
```

## Contoh Query

### Insert Data
```sql
INSERT INTO market_data (
    emiten, url, date_time_scraping, last_update_text,
    price, high_price, low_price, last_price, open_price
) VALUES (
    'BBCA',
    'https://katadata.co.id/saham/bbca',
    '2025-01-22 14:30:00+07',
    '2025-01-22 14:25:00+07',
    9250.00,
    9300.00,
    9200.00,
    9250.00,
    9225.00
);
```

### Select Latest Data per Emiten
```sql
SELECT * FROM v_latest_market_data ORDER BY emiten;
```

### Select Data by Emiten
```sql
SELECT * FROM market_data
WHERE emiten = 'BBCA'
ORDER BY date_time_scraping DESC
LIMIT 10;
```

### Select Data by Date Range
```sql
SELECT * FROM market_data
WHERE date_time_scraping >= '2025-01-01'
  AND date_time_scraping < '2025-02-01'
ORDER BY date_time_scraping DESC;
```

### Get Average Price per Emiten
```sql
SELECT
    emiten,
    AVG(price) as avg_price,
    MAX(high_price) as max_price,
    MIN(low_price) as min_price,
    COUNT(*) as data_points
FROM market_data
WHERE date_time_scraping >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY emiten
ORDER BY emiten;
```
