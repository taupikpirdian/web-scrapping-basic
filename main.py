"""Main entry point for the market data scraper."""

import argparse
import json
import os

from src.models.database import save_market_data
from src.services.market_scraper import scrape_market


def main() -> None:
    """Main function untuk menjalankan scraper."""
    parser = argparse.ArgumentParser(description="Scrape market data dari Katadata")
    parser.add_argument(
        "--save-db",
        action="store_true",
        help="Simpan data ke database (memerlukan konfigurasi environment variable)"
    )

    args = parser.parse_args()

    # Ambil daftar emiten dari environment variable
    # Format: EMITEN_LIST=bbca,indf,tlkm
    emiten_env = os.getenv("EMITEN_LIST", "bbca,indf")
    emiten_list = [e.strip() for e in emiten_env.split(",") if e.strip()]

    data_list = []
    saved_ids = []

    print(f"Memproses emiten: {', '.join(emiten_list)}")

    for emiten in emiten_list:
        try:
            market_data = scrape_market(emiten)
            data_list.append(market_data.to_dict())

            # Simpan ke database jika flag --save-db diberikan
            if args.save_db:
                try:
                    record_id = save_market_data(
                        emiten=market_data.emiten,
                        url=market_data.url,
                        date_time_scraping=market_data.date_time_scraping,
                        price=market_data.price,
                        high_price=market_data.high_price,
                        low_price=market_data.low_price,
                        last_price=market_data.last_price,
                        open_price=market_data.open_price,
                        last_update_text=market_data.last_update_text
                    )
                    saved_ids.append(record_id)
                    print(f"✓ Data {market_data.emiten} berhasil disimpan ke database (ID: {record_id})")
                except Exception as e:
                    print(f"✗ Gagal menyimpan data {market_data.emiten} ke database: {e}")

        except Exception as e:
            print(f"✗ Gagal scrape data untuk {emiten}: {e}")

    # Simpan ke file JSON
    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(f"\nData yang berhasil di-scrape: {len(data_list)}")
    if args.save_db and saved_ids:
        print(f"Data yang berhasil disimpan ke database: {len(saved_ids)}")
    print(json.dumps(data_list, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
