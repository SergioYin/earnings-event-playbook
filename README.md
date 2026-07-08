# earnings-event-playbook

Build deterministic earnings event playbooks from local JSON fixtures for analysts, investors, and research teams who want repeatable pre-earnings and post-event review packets without wiring up data vendors or broker systems.

Star this repo if you want a small, auditable example of turning static earnings-calendar, consensus, and portfolio fixtures into Markdown, JSON, and a no-JavaScript HTML review artifact.

Zero-dependency Python package and CLI. No API keys, no live market data, no broker connection, no order placement, no database, no JavaScript requirement for the demo page, and no investment advice.

## First Look

- Target user: a research operator who wants a local, deterministic checklist before earnings events.
- Value in 2 minutes: open `demo/index.html`, `demo/playbook.md`, `demo/post-event-compare.md`, or `demo/handoff.md` to see scenario bands, source freshness, attention scores, actuals comparisons, thesis sensitivities, review queues, and cross-asset handoff packs.
- Star reason: useful as a public, dependency-free template for finance research artifacts with explicit safety boundaries and release evidence.

## Quickstart

```bash
python -m pip install -e .
earnings-event-playbook demo-bundle --out demo
earnings-event-playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
earnings-event-playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
earnings-event-playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
earnings-event-playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
earnings-event-playbook selfcheck
```

Without installation:

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
```

Open `demo/index.html` in a browser for the static preview, or read `demo/playbook.md`, `demo/playbook.json`, `demo/post-event-compare.md`, `demo/post-event-compare.json`, `demo/visual-receipt.md`, `demo/visual-receipt.json`, `demo/handoff.md`, and `demo/handoff.json`.

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
- Post-event actual EPS, revenue, and move outcomes.
- Thesis-ledger handoff notes and review queue status.
- Cross-asset handoff packs for thesis-ledger and earnings-call-risk-map style workflows.
- Optional evidence artifact hashes carried from a local visual receipt.

## Examples

Bundled fixtures live in `examples/events.json`, `examples/portfolio.json`, and `examples/actuals.json`.

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

That writes `events.json`, `portfolio.json`, `actuals.json`, `playbook.md`, `playbook.json`, `post-event-compare.md`, `post-event-compare.json`, `index.html`, `visual-receipt.md`, `visual-receipt.json`, `handoff.md`, and `handoff.json`.

Compare a pre-event playbook to local post-event actuals:

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event \
  --before-playbook demo/playbook.json \
  --actuals examples/actuals.json \
  --out demo/post-event-compare.md \
  --json-out demo/post-event-compare.json
```

That writes a descriptive post-event comparison with EPS, revenue, and move outcomes, matched scenario bands, thesis-ledger handoff notes, and review status. It does not recommend any action.

Create a visual evidence receipt for checked-in demo artifacts:

```bash
PYTHONPATH=src python -m earnings_event_playbook visual-receipt \
  --artifacts demo \
  --out demo/visual-receipt.md \
  --json-out demo/visual-receipt.json
```

The receipt scans local HTML, Markdown, and JSON demo artifacts, records each file role, byte size, SHA-256 hash, regeneration commands, review checklist, and safety boundaries. Receipt and handoff outputs are excluded from the receipt inventory so reruns stay deterministic and avoid circular handoff hashes.

Export thesis-ledger and earnings-call-risk-map style handoff packs:

```bash
PYTHONPATH=src python -m earnings_event_playbook export-handoff \
  --playbook demo/playbook.json \
  --post-event-compare demo/post-event-compare.json \
  --visual-receipt demo/visual-receipt.json \
  --out demo/handoff.md \
  --json-out demo/handoff.json
```

The handoff schema includes ticker, fiscal period, source freshness, open review items, thesis note draft, risk map prompts, catalyst follow-up, and optional evidence artifact hashes from the visual receipt. It is descriptive handoff material and does not recommend any action.

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

`actuals.json` contains `as_of` and an `actuals` list with report date, actual EPS, actual revenue, actual move percent, source metadata, and optional notes.

`handoff.json` contains `schema_version`, `artifact`, `workflows`, safety boundaries, and `handoff_packs` with ticker, company, fiscal period, source freshness, event source, actual source, review status, open review items, thesis note draft, risk map prompts, catalyst follow-up, and evidence artifact hashes when `--visual-receipt` is provided.

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
