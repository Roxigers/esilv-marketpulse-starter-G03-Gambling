
from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.yahoo_provider import fetch_yahoo_prices


DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER_LABEL = "Yahoo Finance"

YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def display_market_summary(asset, prices, show_currency=True):
    suffix = f" {asset['currency']}" if show_currency else ""
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{suffix}")
    print(f"Last close   : {get_last_close(prices):.2f}{suffix}")


def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_symbol = YAHOO_SYMBOLS[instrument["ticker"]]
    benchmark_symbol = YAHOO_SYMBOLS[benchmark["ticker"]]

    instrument_prices = fetch_yahoo_prices(
        instrument_symbol,
        instrument["ticker"],
    )

    benchmark_prices = fetch_yahoo_prices(
        benchmark_symbol,
        benchmark["ticker"],
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:
        raise ValueError("No common observation dates found")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print(f"Provider : {PROVIDER_LABEL}")
    print()
    print("Instrument")
    display_market_summary(instrument, aligned_instrument)
    print(f"Period return : {instrument_return:.2f}%")
    print()
    print("Benchmark")
    display_market_summary(benchmark, aligned_benchmark, show_currency=False)
    print(f"Period return : {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    relative_sign = "+" if relative_performance >= 0 else ""
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_sign}{relative_performance:.2f} percentage points"
    )
    print()
    print("Base 100")
    print(
        f"{instrument['ticker']}  : "
        f"{instrument_base_100[0]['value']:.2f} -> "
        f"{instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark['ticker']} : "
        f"{benchmark_base_100[0]['value']:.2f} -> "
        f"{benchmark_base_100[-1]['value']:.2f}"
    )


if __name__ == "__main__":
    main()
