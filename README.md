# ESILV MarketPulse

[![Course: MESIFI472326](https://img.shields.io/badge/course-MESIFI472326-1f6feb.svg)](https://www.python.org/)
[![ESILV A4](https://img.shields.io/badge/ESILV-A4-111827.svg)](https://www.python.org/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)](https://www.python.org/)

## What is MarketPulse?

MarketPulse is the ESILV A4 "Python, Git, Linux" team project. It compares one
instrument with its benchmark over one month of daily data, and presents the same
application result in the terminal and in a Dash dashboard.

- Instrument: AAPL - Apple Inc.
- Benchmark: SP500 - S&P 500
- Lookback: 1 month
- Interval: Daily
- Indicators: period return, relative performance (percentage points), base 100

## Provider and access mode

The final run uses **Bloomberg stage - APPROVED_SAMPLE**: data is read from the
approved sample file `data/sample/bloomberg_reference_sample.json` and normalized to
the canonical row format. It is not a LIVE Bloomberg connection.

A Yahoo Finance provider (via `yfinance`) is also included in `src/providers/`.

## Architecture

```text
providers -> canonical rows -> analytics.py -> build_market_snapshot() -> terminal / Dash
```

```text
src/
  main.py            build_market_snapshot() + terminal output
  analytics.py       alignment, period return, relative performance, base 100
  dashboard.py       Dash presentation only
  providers/
    bloomberg_provider.py
    yahoo_provider.py
```

## Install

```bash
python -m pip install -r requirements.txt
```

## Run

Run both commands from the repository root.

Terminal:

```bash
python src/main.py
```

Dashboard (then open http://127.0.0.1:8050/ in a browser; in GitHub Codespaces,
open port 8050 from the Ports tab):

```bash
python src/dashboard.py
```

## Environment constraints

- Commands must be run from the repository root (data paths are relative).
- The default path needs no network and no credentials: it reads the approved sample.
- A real Bloomberg LIVE access would require the authorized classroom environment.
- No secret or credential is stored in this repository.

## Evidence

Checkpoint evidence is stored in `evidence/checkpoint-<letter>/<github-username>/`.

## Team

See [TEAM.md](TEAM.md).