
# Bloomberg Field Mapping - TD09

Student: Leyan Very
Team: G03 - Gambling

## 1. Access mode

APPROVED_SAMPLE

Source: data/sample/bloomberg_reference_sample.json

Expected reference: data/sample/bloomberg_reference_expected.json

Live Bloomberg connectivity: Not demonstrated.

The sample contains illustrative teaching data, not verified live Bloomberg market data.

## 2. Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The analytics layer must always use the canonical tickers AAPL and SP500.

## 3. Inspected sample data

Both instruments contain 21 daily observations from 2026-09-01 to 2026-09-30.

The input structure contains a series list, with an observations list for each instrument.

Available fields:
- observation_date
- open_value
- high_value
- low_value
- close_value
- volume_value

These are teaching wrapper keys, not official Bloomberg field mnemonics.

## 4. Field mapping

| MarketPulse field | Sample field | Conversion |
|---|---|---|
| date | observation_date | Keep YYYY-MM-DD string |
| ticker | canonical_ticker | Keep AAPL or SP500 |
| open | open_value | float |
| high | high_value | float |
| low | low_value | float |
| close | close_value | float |
| volume | volume_value | int |

No missing fields were observed in the approved sample. The SP500 volume is zero in this dataset.

## 5. TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity
- Benchmark identifier: SPX Index
- Date representation: YYYY-MM-DD
- Input structure: series[] containing observations[]
- Missing fields: None observed
- Special normalization: Convert prices to float and volume to int.
- Preserve canonical tickers AAPL and SP500.
- Keep provider-specific identifiers outside analytics.py.
- Expected output: data/sample/bloomberg_reference_expected.json

TD10 will implement the Bloomberg sample provider using this mapping.
