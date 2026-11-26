# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`
- Live connectivity: not demonstrated
- The sample states `is_live_bloomberg_output: false`. It contains illustrative
  teaching values and is not certified Bloomberg historical data.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

Provider identifiers by stage:

| Canonical | CSV | Yahoo | Bloomberg |
|---|---|---|---|
| AAPL | AAPL | AAPL | AAPL US Equity |
| SP500 | SP500 | ^GSPC | SPX Index |

The analytical layer keeps receiving `AAPL` and `SP500`, never a provider identifier.

## Inspected inputs

### Instrument: `AAPL US Equity` (canonical ticker `AAPL`)

- 21 observations, from 2026-09-01 to 2026-09-30
- Date representation: string `YYYY-MM-DD` in `observation_date`
- Structure: `series[]` entries with `role`, `canonical_ticker`,
  `provider_identifier` and a list `observations[]`
- Available fields: `observation_date`, `open_value`, `high_value`,
  `low_value`, `close_value`, `volume_value`
- Missing values: none observed

### Benchmark: `SPX Index` (canonical ticker `SP500`)

- 21 observations, from 2026-09-01 to 2026-09-30
- Same structure and same fields as the instrument
- Missing values: none observed, but `volume_value` is `0` for every
  observation (an index has no traded volume in this sample)

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Already `YYYY-MM-DD`, no conversion needed |
| ticker | application mapping | `AAPL` or `SP500`, taken from `canonical_ticker`, not from the Bloomberg identifier |
| open | `open_value` | Teaching wrapper key; convert to float |
| high | `high_value` | Teaching wrapper key; convert to float |
| low | `low_value` | Teaching wrapper key; convert to float |
| close | `close_value` | Teaching wrapper key; convert to float |
| volume | `volume_value` | Teaching wrapper key; convert to int; `0` for the benchmark |

Teaching wrapper key != Bloomberg LIVE field mnemonic. The keys above exist only
in the approved sample. No LIVE Bloomberg field name was observed in this
session, so none is recorded here.

## Canonical row target

```python
{
    "date": "2026-09-01",
    "ticker": "SP500",
    "open": 6592.0,
    "high": 6615.0,
    "low": 6580.0,
    "close": 6600.0,
    "volume": 0,
}
```

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: `AAPL US Equity` (canonical `AAPL`)
- Benchmark identifier: `SPX Index` (canonical `SP500`)
- Date representation: string `YYYY-MM-DD`
- Input structure: `series[]` with `observations[]`, one dictionary per day
- Missing fields: none in the sample; the benchmark volume is always `0`
- Special normalization notes: convert prices to float and volume to int;
  use `canonical_ticker` for the `ticker` field; keep Bloomberg identifiers
  inside the provider module only
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json`