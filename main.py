"""Main entry point for the market data scraper."""

import json

from src.services.market_scraper import scrape_market


def main() -> None:
    """Main function untuk menjalankan scraper."""
    data_list = []
    emiten_list = [
        "bbca",
        "indf"
    ]

    for emiten in emiten_list:
        market_data = scrape_market(emiten)
        data_list.append(market_data.to_dict())

    with open("market_data.json", "w", encoding="utf-8") as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)

    print(data_list)
    print(f"\nSelesai. Data Market: {len(data_list)}")


if __name__ == "__main__":
    main()
