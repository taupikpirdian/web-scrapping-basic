"""Database models dan functions untuk menyimpan data scraping ke MySQL."""

import os
from typing import Optional

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "myorbit_market_data")


def save_market_data(emiten: str, url: str, date_time_scraping: str,
                     price: Optional[float], high_price: Optional[float],
                     low_price: Optional[float], last_price: Optional[float],
                     open_price: Optional[float], last_update_text: Optional[str]) -> int:
    """Simpan data market hasil scraping ke database MySQL.

    Args:
        emiten: Kode saham emiten
        url: URL sumber data
        date_time_scraping: Waktu scraping dilakukan (ISO format atau DATETIME string)
        price: Harga saat ini
        high_price: Harga tertinggi
        low_price: Harga terendah
        last_price: Harga terakhir
        open_price: Harga pembukaan
        last_update_text: Text waktu update terakhir

    Returns:
        ID dari record yang baru disimpan

    Raises:
        ImportError: Jika mysql-connector-python tidak terinstall
        Exception: Jika koneksi atau penyimpanan gagal
    """
    try:
        import mysql.connector
    except ImportError:
        raise ImportError("mysql-connector-python belum terinstall. Install dengan: pip install mysql-connector-python")

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )
        cursor = conn.cursor()

        query = """
            INSERT INTO market_data (
                emiten, url, date_time_scraping, last_update_text,
                price, high_price, low_price, last_price, open_price
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """
        cursor.execute(query, (
            emiten, url, date_time_scraping, last_update_text,
            price, high_price, low_price, last_price, open_price
        ))

        conn.commit()
        record_id = cursor.lastrowid

        cursor.close()
        conn.close()

        return record_id

    except Exception as e:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        raise Exception(f"Gagal menyimpan data ke database: {e}")
