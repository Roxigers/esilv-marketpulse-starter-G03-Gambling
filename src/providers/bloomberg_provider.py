import json
from pathlib import Path

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

ACCESS_MODE = "APPROVED_SAMPLE"


def load_bloomberg_sample(canonical_ticker):
    file_path = (
        Path(__file__).resolve().parents[2]
        / "data/sample/bloomberg_reference_sample.json"
    )

    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)

    if data["access_mode"] != "approved_sample":
        raise ValueError("Unexpected Bloomberg access mode")

    for series in data["series"]:
        if series["canonical_ticker"] == canonical_ticker:
            return series["observations"]

    raise ValueError(f"No data found for {canonical_ticker}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for observation in raw_data:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(f"Unsupported ticker: {canonical_ticker}")

    raw_data = load_bloomberg_sample(canonical_ticker)

    return normalize_bloomberg_history(
        raw_data,
        canonical_ticker,
    )
