from pathlib import Path
import csv
import json

from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices
from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


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
    if not prices:
        raise ValueError("No prices available.")
    return float(prices[0]["close"])


def get_last_close(prices):
    if not prices:
        raise ValueError("No prices available.")
    return float(prices[-1]["close"])


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def display_market_summary(asset, prices, show_currency=True):
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(
        "First close  : "
        + f"{first_close:.2f}"
        + (f" {asset['currency']}" if show_currency else "")
    )
    print(
        "Last close   : "
        + f"{last_close:.2f}"
        + (f" {asset['currency']}" if show_currency else "")
    )


def main():
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period="1mo",
        interval="1d",
    )
    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period="1mo",
        interval="1d",
    )

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print("Yahoo Finance via yfinance")
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()
    print("Instrument")
    display_market_summary(instrument, instrument_prices)
    print()
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)
    print()

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices, benchmark_prices
    )
    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative = calculate_relative_performance(instrument_return, benchmark_return)
    instrument_base = calculate_base_100(aligned_instrument)
    benchmark_base = calculate_base_100(aligned_benchmark)

    print("Period return")
    print(f"{instrument['ticker']}: {instrument_return:.2f}%")
    print(f"{benchmark['ticker']}: {benchmark_return:.2f}%")
    print()
    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']}: {relative:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument['ticker']}: {instrument_base[0]['value']:.2f} -> {instrument_base[-1]['value']:.2f}")
    print(f"{benchmark['ticker']}: {benchmark_base[0]['value']:.2f} -> {benchmark_base[-1]['value']:.2f}")


if __name__ == "__main__":
    main()