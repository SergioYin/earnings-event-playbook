# earnings-event-playbook

Build deterministic earnings event playbooks from local JSON fixtures for analysts, investors, and research teams who want a repeatable pre-earnings review packet without wiring up data vendors or broker systems.

Star this repo if you want a small, auditable example of turning static earnings-calendar, consensus, and portfolio fixtures into Markdown, JSON, and a no-JavaScript HTML review artifact.

Zero-dependency Python package and CLI. No API keys, no live market data, no broker connection, no order placement, no database, no JavaScript requirement for the demo page, and no investment advice.

## First Look

- Target user: a research operator who wants a local, deterministic checklist before earnings events.
- Value in 2 minutes: open `demo/index.html` or `demo/playbook.md` to see scenario bands, source freshness, attention scores, thesis sensitivities, and a post-event review queue.
- Star reason: useful as a public, dependency-free template for finance research artifacts with explicit safety boundaries and release evidence.

## Quickstart

```bash
python -m pip install -e .
earnings-event-playbook demo-bundle --out demo
earnings-event-playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
earnings-event-playbook selfcheck
```

Without installation:

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
```

Open `demo/index.html` in a browser for the static preview, or read `demo/playbook.md` and `demo/playbook.json`.

Expected output: a review packet for the bundled EXM and NXT example events with beat/base/miss exposure bands, stale-source warnings, risk questions, and deterministic JSON for downstream local tooling.

## What It Models

- Earnings event date, ticker, company, and fiscal period.
- Consensus EPS and revenue from static fixture fields.
- Implied move percent.
- Portfolio position, exposure, and portfolio weight fixtures.
- Thesis sensitivity notes.
- Source freshness labels.
- Beat, base, and miss scenario bands.
- Risk questions and post-event review queue.

## Examples

Bundled fixtures live in `examples/events.json` and `examples/portfolio.json`.

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook \
  --events examples/events.json \
  --portfolio examples/portfolio.json \
  --out demo/playbook.md \
  --json-out demo/playbook.json
```

Generate a complete local demo bundle:

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
```

That writes `events.json`, `portfolio.json`, `playbook.md`, `playbook.json`, and `index.html`.

## Safety Boundaries

This project is a local research organization tool.

- It uses local static fixtures only.
- It does not fetch live data.
- It does not connect to brokers.
- It does not place, stage, or recommend orders.
- It does not provide personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Outputs should be reviewed against source materials before use.

It is intentionally not a trading bot, data vendor client, portfolio optimizer, alerting system, or compliance system.

## Schema Sketch

`events.json` contains `as_of`, an `events` list, optional `thesis_sensitivities`, and optional `risk_questions`.

`portfolio.json` contains `as_of`, `base_currency`, and a `positions` list.

The parser is intentionally small and strict so fixture errors fail early.

## Development

```bash
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m unittest discover
PYTHONPATH=src python -m earnings_event_playbook selfcheck
uv build
```

Runtime dependencies: `0`.

GitHub Actions workflows are intentionally not included.

## Release Evidence

See `docs/release-readiness.md` for the maturity evidence checklist, verification commands, package boundary notes, and known risk limits.
