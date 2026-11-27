# Bloomberg Field Mapping

## 1. Purpose

This document defines the mapping contract between the Bloomberg reference
input and the canonical MarketPulse data format.

It is a handoff document for TD10. It does not implement a Bloomberg provider.

## 2. Access mode

**Selected mode: `APPROVED_SAMPLE`**

The repository contains an approved fallback sample fixture. This work does
not demonstrate live Bloomberg connectivity.

The sample identifies itself as an instructor-approved fallback fixture.
Its values are illustrative teaching values reused from
`data/sample/prices.csv`; they are not certified Bloomberg historical
observations.

## 3. Source files and limitations

Input fixture:

- `data/sample/bloomberg_reference_sample.json`

Expected canonical output:

- `data/sample/bloomberg_reference_expected.json`

The separate instructor reference document
`docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` was not present in this
repository checkout.

The mapping below is therefore based on the actual sample fixture and its
metadata.

## 4. Instrument and benchmark identifiers

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | `AAPL` | `AAPL US Equity` |
| Benchmark | `SP500` | `SPX Index` |

The canonical tickers must be preserved in MarketPulse output.
Bloomberg identifiers must not replace canonical tickers.

## 5. Input structure

The sample contains a `series` collection.

Each series includes:

- `role`: identifies the instrument or benchmark.
- `canonical_ticker`: MarketPulse ticker.
- `provider_identifier`: Bloomberg-style identifier.
- `observations`: collection of observations.

Both the instrument and benchmark contain 21 observations in the sample.

## 6. Field mapping

| MarketPulse canonical field | Sample input field | Mapping rule |
|---|---|---|
| `date` | `observation_date` | Preserve the observation date |
| `ticker` | `canonical_ticker` | Preserve `AAPL` or `SP500` |
| `open` | `open_value` | Map opening value |
| `high` | `high_value` | Map highest value |
| `low` | `low_value` | Map lowest value |
| `close` | `close_value` | Map closing value |
| `volume` | `volume_value` | Map trading volume |

**Important:** These source field names are wrapper keys in the teaching
fixture. They are not verified Bloomberg field mnemonics.

No unverified Bloomberg field mnemonics are specified in this document.

## 7. Canonical output contract

TD10 must normalize observations to the following MarketPulse structure:

```json
{
  "date": "YYYY-MM-DD",
  "ticker": "AAPL",
  "open": 0,
  "high": 0,
  "low": 0,
  "close": 0,
  "volume": 0
}


```

For benchmark observations, the canonical ticker must be `SP500`.

The values above illustrate the structure only; they are not market data.

## 8. Data quality and limitations

- The sample contains 21 observations for each series.
- The observed sample fields are `observation_date`, `open_value`,
  `high_value`, `low_value`, `close_value`, and `volume_value`.
- The fixture is not live Bloomberg output.
- The sample's teaching values must not be presented as certified   
  Bloomberg historical data.
- Actual Bloomberg field mnemonics and live access details remain
  unverified.

## 9. TD10 handoff

The TD10 implementation should:

1. Read the approved sample fixture or the instructor-approved Bloomberg
   source made available later.
2. Identify the instrument and benchmark using their provider identifiers.
3. Preserve canonical tickers `AAPL` and `SP500`.
4. Normalize observations to the canonical MarketPulse fields.
5. Keep provider-specific logic inside the Bloomberg provider boundary.
6. Reuse the existing analytics layer rather than changing its contract.
7. Avoid committing credentials, tokens, or session information.

## 10. Conclusion

This document establishes the mapping contract for the `APPROVED_SAMPLE`
mode. It does not claim that a live Bloomberg connection has been tested.
