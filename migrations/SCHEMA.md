# Database Schema - Market Data Scraper

## Table: market_data

Tabel utama untuk menyimpan data hasil scraping harga saham dari Katadata.

### Struktur Kolom

| Kolom | Tipe Data | Deskripsi |
|-------|-----------|-----------|
| `id` | BIGINT UNSIGNED AUTO_INCREMENT | Primary key |
| `emiten` | VARCHAR(10) | Kode saham emiten (contoh: BBCA, INDF) |
| `url` | TEXT | URL sumber data scraping |
| `date_time_scraping` | DATETIME | Waktu ketika scraping dilakukan |
| `last_update_text` | DATETIME | Waktu update terakhir dari sumber data |
| `price` | DECIMAL(18, 2) | Harga saham saat ini |
| `high_price` | DECIMAL(18, 2) | Harga tertinggi |
| `low_price` | DECIMAL(18, 2) | Harga terendah |
| `last_price` | DECIMAL(18, 2) | Harga terakhir |
| `open_price` | DECIMAL(18, 2) | Harga pembukaan |
| `created_at` | DATETIME | Waktu record dibuat di database |
| `updated_at` | DATETIME | Waktu record terakhir diupdate (auto-update) |
| `deleted_at` | DATETIME | Soft delete timestamp |

### Indexes

| Nama Index | Kolom | Tipe | Deskripsi |
|------------|-------|------|-----------|
| PRIMARY | id | BTREE | Primary key |
| idx_emiten | emiten | BTREE | Index pada kode emiten untuk filtering cepat |
| idx_date_time_scraping | date_time_scraping | BTREE | Index pada waktu scraping untuk sorting |
| idx_emiten_date | emiten, date_time_scraping | BTREE | Composite index untuk query per emiten berdasarkan waktu |
| idx_last_update | last_update_text | BTREE | Index pada waktu update terakhir |

### Engine
- **InnoDB** - Support transactions dan foreign keys

### Character Set
- **utf8mb4** - Support penuh Unicode termasuk emoji
- **Collation**: utf8mb4_general_ci - Case-insensitive comparison

## View: v_latest_market_data

View untuk mendapatkan data terbaru per emiten tanpa perlu menulis subquery complex.

### Kolom
Sama dengan tabel market_data, hanya menampilkan 1 record terbaru per emiten berdasarkan `date_time_scraping`.

### Query Definition
```sql
SELECT
    t1.id,
    t1.emiten,
    t1.url,
    t1.date_time_scraping,
    t1.last_update_text,
    t1.price,
    t1.high_price,
    t1.low_price,
    t1.last_price,
    t1.open_price,
    t1.created_at,
    t1.updated_at
FROM market_data t1
INNER JOIN (
    SELECT emiten, MAX(date_time_scraping) as max_date
    FROM market_data
    WHERE deleted_at IS NULL
    GROUP BY emiten
) t2 ON t1.emiten = t2.emiten AND t1.date_time_scraping = t2.max_date
WHERE t1.deleted_at IS NULL
ORDER BY t1.emiten;
```

## Contoh Query

### 1. Insert Data
```sql
INSERT INTO market_data (
    emiten, url, date_time_scraping, last_update_text,
    price, high_price, low_price, last_price, open_price
) VALUES (
    'BBCA',
    'https://katadata.co.id/saham/bbca',
    '2025-01-22 14:30:00',
    '2025-01-22 14:25:00',
    9250.00,
    9300.00,
    9200.00,
    9250.00,
    9225.00
);
```

### 2. Select Latest Data per Emiten (menggunakan View)
```sql
SELECT * FROM v_latest_market_data
WHERE emiten IN ('BBCA', 'INDF', 'TLKM')
ORDER BY emiten;
```

### 3. Select Historical Data untuk Emiten Tertentu
```sql
SELECT
    date_time_scraping,
    price,
    high_price,
    low_price,
    open_price
FROM market_data
WHERE emiten = 'BBCA'
  AND deleted_at IS NULL
  AND date_time_scraping >= DATE_SUB(NOW(), INTERVAL 7 DAY)
ORDER BY date_time_scraping DESC;
```

### 4. Statistik Harga per Emiten
```sql
SELECT
    emiten,
    COUNT(*) as total_records,
    MAX(price) as max_price,
    MIN(price) as min_price,
    AVG(price) as avg_price,
    MAX(date_time_scraping) as latest_scraping
FROM market_data
WHERE deleted_at IS NULL
GROUP BY emiten
ORDER BY emiten;
```

### 5. Cari Emiten dengan Perubahan Harga Terbesar
```sql
SELECT
    emiten,
    price as current_price,
    open_price as opening_price,
    ((price - open_price) / open_price * 100) as price_change_percent,
    date_time_scraping
FROM market_data
WHERE deleted_at IS NULL
  AND date_time_scraping = (
      SELECT MAX(date_time_scraping)
      FROM market_data m2
      WHERE m2.emiten = market_data.emiten
        AND m2.deleted_at IS NULL
  )
ORDER BY ABS(price_change_percent) DESC
LIMIT 10;
```

### 6. Soft Delete Record
```sql
UPDATE market_data
SET deleted_at = NOW()
WHERE id = 123;
```

### 7. Hard Delete (Permanent - hati-hati)
```sql
DELETE FROM market_data
WHERE deleted_at IS NOT NULL
  AND deleted_at < DATE_SUB(NOW(), INTERVAL 30 DAY);
```

## Best Practices

1. **Selalu gunakan WHERE deleted_at IS NULL** untuk query data aktif
2. **Gunakan view v_latest_market_data** untuk mengambil data terbaru per emiten
3. **Index idx_emiten_date** sudah optimized untuk query filter berdasarkan emiten dan sorting berdasarkan waktu
4. **Soft delete** dengan mengisi `deleted_at` instead of menghapus record langsung
5. **DECIMAL(18, 2)** digunakan untuk presisi harga saham (support sampai 999 trillion)

## Migration Files

- **001_create_market_data_table_mysql.sql** - Create table dan view
- **001_rollback_market_data_table_mysql.sql** - Rollback (drop table dan view)
- **run_migration.py** - Python script untuk menjalankan migration

## Notes

- Tabel mengikuti pattern database `myorbit_payment` yang sudah ada
- Menggunakan soft delete pattern dengan kolom `deleted_at`
- Auto-update timestamp untuk kolom `updated_at`
- Character set utf8mb4 untuk support karakter Indonesia dan emoji
