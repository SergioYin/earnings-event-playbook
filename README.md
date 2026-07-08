# earnings-event-playbook

Build deterministic earnings event playbooks from local JSON fixtures for analysts, investors, and research teams who want repeatable pre-earnings and post-event review packets without wiring up data vendors or broker systems.

Star this repo if you want a small, auditable example of turning static earnings-calendar, consensus, and portfolio fixtures into Markdown, JSON, no-JavaScript HTML review artifacts, and release-evidence manifests.

Zero-dependency Python package and CLI. No API keys, no live market data, no broker connection, no order placement, no database, no JavaScript requirement for the demo page, and no investment advice.

## First Look

- Target user: a research operator who wants a local, deterministic checklist before earnings events.
- Value in 2 minutes: open `demo/showcase.html` and `docs/showcase.md` for the complete landing overview, then open `docs/tutorial-software-case.md` and `demo/tutorial-bundle.md` for the software case walkthrough.
- Showcase manifest: read `demo/showcase.json` for value proposition, quickstart commands, artifact links, release evidence, maturity rubric, case highlights, tutorial path, risk boundaries, and star-worthy differentiation.
- Tutorial CTA: run `earnings-event-playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json` to regenerate the ordered software case packet.
- Multi-case fixture gallery: open `demo/fixture-gallery.md` or `demo/fixture-gallery.json` to compare the software, retail, and semiconductor case fixtures.
- Scenario notebook: open `demo/scenario-notebook.md` or `demo/scenario-notebook.json` for the combined reviewer packet across playbook, handoff, gallery, tutorial, and showcase artifacts.
- Portfolio drift bridge: open `demo/portfolio-drift-bridge.md` or `demo/portfolio-drift-bridge.json` for exposure concentration, event-linked tickers, scenario mismatches, post-event drift watchlist, next risk review prompts, and no-trade boundaries.
- Review packet: open `docs/review-packet.md` and `demo/review-packet/review-packet-manifest.json` for the deterministic release packet, manifest schema, file roles, and SHA-256 hash inventory.
- Cold-start audit: open `docs/coldstart-audit.md`, `demo/coldstart-audit.md`, and `demo/coldstart-audit.json` for clone-read-run-trust-promote readiness scoring across README, docs, demo artifacts, and the review packet manifest.
- Evidence ledger: open `docs/evidence-ledger.md`, `demo/evidence-ledger.md`, and `demo/evidence-ledger.json` for the maintainer evidence ledger across release manifest, review packet manifest, cold-start audit, and git commit metadata when available.
- Star reason: useful as a public, dependency-free template for finance research artifacts with explicit safety boundaries and release evidence.

## Quickstart

```bash
python -m pip install -e .
earnings-event-playbook demo-bundle --out demo
earnings-event-playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
earnings-event-playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
earnings-event-playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
earnings-event-playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
earnings-event-playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out demo/fixture-gallery.md --json-out demo/fixture-gallery.json
earnings-event-playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json
earnings-event-playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json
earnings-event-playbook scenario-notebook --playbook demo/playbook.json --handoff demo/handoff.json --fixture-gallery demo/fixture-gallery.json --manifest demo/tutorial-bundle.json demo/showcase.json --out demo/scenario-notebook.md --json-out demo/scenario-notebook.json
earnings-event-playbook portfolio-drift-bridge --portfolio examples/portfolio.json --scenario-notebook demo/scenario-notebook.json --post-event-compare demo/post-event-compare.json --risk-thresholds examples/risk-thresholds.json --out demo/portfolio-drift-bridge.md --json-out demo/portfolio-drift-bridge.json
earnings-event-playbook review-packet --out demo/review-packet
earnings-event-playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json
earnings-event-playbook evidence-ledger --release-manifest release_manifest.json --review-manifest demo/review-packet/review-packet-manifest.json --coldstart-audit demo/coldstart-audit.json --out demo/evidence-ledger.md --json-out demo/evidence-ledger.json
earnings-event-playbook selfcheck
```

Without installation:

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out demo/fixture-gallery.md --json-out demo/fixture-gallery.json
PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json
PYTHONPATH=src python -m earnings_event_playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json
PYTHONPATH=src python -m earnings_event_playbook scenario-notebook --playbook demo/playbook.json --handoff demo/handoff.json --fixture-gallery demo/fixture-gallery.json --manifest demo/tutorial-bundle.json demo/showcase.json --out demo/scenario-notebook.md --json-out demo/scenario-notebook.json
PYTHONPATH=src python -m earnings_event_playbook portfolio-drift-bridge --portfolio examples/portfolio.json --scenario-notebook demo/scenario-notebook.json --post-event-compare demo/post-event-compare.json --risk-thresholds examples/risk-thresholds.json --out demo/portfolio-drift-bridge.md --json-out demo/portfolio-drift-bridge.json
PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet
PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json
PYTHONPATH=src python -m earnings_event_playbook evidence-ledger --release-manifest release_manifest.json --review-manifest demo/review-packet/review-packet-manifest.json --coldstart-audit demo/coldstart-audit.json --out demo/evidence-ledger.md --json-out demo/evidence-ledger.json
```

Open `demo/showcase.html` for the no-JavaScript landing page, `demo/showcase.json` for the manifest, `docs/tutorial-software-case.md` and `demo/tutorial-bundle.md` for the software case walkthrough, `demo/scenario-notebook.md` for the combined reviewer notebook, `demo/portfolio-drift-bridge.md` for portfolio drift bridge review, `demo/review-packet/review-packet-manifest.json` for release packet evidence, `demo/coldstart-audit.md` for clone-read-run-trust-promote readiness, `demo/evidence-ledger.md` for maintainer release evidence, `demo/index.html` for the static preview, or read the paired Markdown and JSON demo artifacts.

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
- Multi-case fixture gallery summaries for checked-in case directories.
- Deterministic tutorial packets with ordered commands, expected artifact paths, reviewer checklist, maturity rubric evidence, and safety boundaries.
- Showcase landing pages with value proposition, artifact map, release evidence, maturity rubric, tutorial path, risk boundaries, and star-worthy differentiation.
- Scenario reviewer notebooks with thesis assumptions, scenario bands, source freshness, evidence hashes, comparison aftermath, next-action queue, risk boundary checklist, and reusable agent prompts.
- Portfolio drift bridge packets with exposure concentration, event-linked tickers, scenario mismatch alerts, post-event drift watchlist, next risk review prompts, static risk thresholds, and no-trade safety boundaries.
- Cold-start audit packets with clone-read-run-trust-promote scores, missing-doc checks, exact quickstart commands, artifact existence and SHA-256 checks, release gate checks, and promotion blockers.
- Maintainer evidence ledgers with release artifacts, commands, maturity rubric mapping, consistency checks, risk boundaries, next evidence requests, and public hygiene flags.

## Examples

Bundled fixtures live in `examples/events.json`, `examples/portfolio.json`, `examples/actuals.json`, and `examples/risk-thresholds.json`.
Multi-case fixtures live in `examples/cases/software`, `examples/cases/retail`, and `examples/cases/semiconductor`.

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

That writes `events.json`, `portfolio.json`, `actuals.json`, `playbook.md`, `playbook.json`, `post-event-compare.md`, `post-event-compare.json`, `index.html`, `visual-receipt.md`, `visual-receipt.json`, `handoff.md`, `handoff.json`, `fixture-gallery.md`, `fixture-gallery.json`, `tutorial-bundle.md`, `tutorial-bundle.json`, `scenario-notebook.md`, `scenario-notebook.json`, `portfolio-drift-bridge.md`, and `portfolio-drift-bridge.json`.

Generate the deterministic release review packet:

```bash
PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet
```

That writes copied static inputs, generated Markdown/HTML/JSON review artifacts, and `demo/review-packet/review-packet-manifest.json` with ordered commands, relative artifact paths, file roles, byte sizes, SHA-256 hashes, release gate checks, promotion notes, and risk boundaries. See `docs/review-packet.md` for the manifest contract and reproducibility check.

Run the cold-start audit against the checked-in review packet:

```bash
PYTHONPATH=src python -m earnings_event_playbook coldstart-audit \
  --manifest demo/review-packet/review-packet-manifest.json \
  --out demo/coldstart-audit.md \
  --json-out demo/coldstart-audit.json
```

That writes Markdown and JSON scoring clone-read-run-trust-promote readiness. The audit reads README, docs, demo paths, and the review packet manifest; records missing-doc checks, exact README quickstart commands, artifact existence and SHA-256 checks, release gates, and promotion blockers.

Generate the maintainer evidence ledger:

```bash
PYTHONPATH=src python -m earnings_event_playbook evidence-ledger \
  --release-manifest release_manifest.json \
  --review-manifest demo/review-packet/review-packet-manifest.json \
  --coldstart-audit demo/coldstart-audit.json \
  --out demo/evidence-ledger.md \
  --json-out demo/evidence-ledger.json
```

That writes Markdown and JSON combining release manifest artifacts, review packet hash inventory, cold-start audit readiness, verification commands, package hygiene, risk boundaries, and next evidence requests. Git metadata is limited to commit identifiers when available.

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

The receipt scans local HTML, Markdown, and JSON demo artifacts, records each file role, byte size, SHA-256 hash, regeneration commands, review checklist, and safety boundaries. Receipt, handoff, and scenario notebook outputs are excluded from the receipt inventory so reruns stay deterministic and avoid circular hashes.

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

Compare multiple local case folders:

```bash
PYTHONPATH=src python -m earnings_event_playbook fixture-gallery \
  --cases examples/cases/software examples/cases/retail examples/cases/semiconductor \
  --out demo/fixture-gallery.md \
  --json-out demo/fixture-gallery.json
```

The gallery summarizes tickers, event counts, stale sources, high attention scores, post-event fixture availability, supported demo commands, and safety boundaries for each case.

Generate the software case tutorial packet:

```bash
PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle \
  --case examples/cases/software \
  --out demo/tutorial-bundle.md \
  --json-out demo/tutorial-bundle.json
```

The packet lists the tutorial article, static fixtures, ordered commands from playbook through fixture gallery, expected artifact paths, reviewer checklist, maturity rubric evidence, and no-advice safety boundaries.

Generate the showcase landing page and manifest:

```bash
PYTHONPATH=src python -m earnings_event_playbook showcase-page \
  --out demo/showcase.html \
  --json-out demo/showcase.json
```

The showcase is a self-contained no-JavaScript HTML landing page plus JSON manifest summarizing the value proposition, quickstart commands, demo artifact links, release evidence, maturity rubric, case gallery highlights, tutorial path, risk boundaries, and star-worthy differentiation.

Generate the scenario reviewer notebook:

```bash
PYTHONPATH=src python -m earnings_event_playbook scenario-notebook \
  --playbook demo/playbook.json \
  --handoff demo/handoff.json \
  --fixture-gallery demo/fixture-gallery.json \
  --manifest demo/tutorial-bundle.json demo/showcase.json \
  --out demo/scenario-notebook.md \
  --json-out demo/scenario-notebook.json
```

The notebook combines generated artifacts into one reviewer packet covering thesis assumptions, scenario bands, source freshness, evidence hashes, comparison aftermath, next-action queue, fixture gallery summary, optional manifest summary, risk boundary checklist, reusable agent prompts, and safety boundaries.

Generate the portfolio drift bridge:

```bash
PYTHONPATH=src python -m earnings_event_playbook portfolio-drift-bridge \
  --portfolio examples/portfolio.json \
  --scenario-notebook demo/scenario-notebook.json \
  --post-event-compare demo/post-event-compare.json \
  --risk-thresholds examples/risk-thresholds.json \
  --out demo/portfolio-drift-bridge.md \
  --json-out demo/portfolio-drift-bridge.json
```

The bridge packet connects static portfolio exposure to scenario-notebook and post-event compare artifacts. It reports concentration flags, event-linked tickers, mismatch alerts, post-event drift watchlist rows, next risk review prompts, threshold values, and no-trade boundaries. It does not recommend any action.

## Safety Boundaries

This project is a local research organization tool.

- It uses local static fixtures only.
- It does not fetch live data.
- It does not connect to brokers.
- It does not place, stage, or recommend orders.
- It does not provide personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Outputs should be reviewed against source materials before use.
- Cold-start audit output is release-readiness evidence, not an audit, compliance report, recommendation, or external validation.
- Evidence ledger output is maintainer release evidence, not an audit, compliance report, recommendation, or external validation.

It is intentionally not a trading bot, data vendor client, portfolio optimizer, alerting system, or compliance system.

## Schema Sketch

`events.json` contains `as_of`, an `events` list, optional `thesis_sensitivities`, and optional `risk_questions`.

`portfolio.json` contains `as_of`, `base_currency`, and a `positions` list.

`actuals.json` contains `as_of` and an `actuals` list with report date, actual EPS, actual revenue, actual move percent, source metadata, and optional notes.

`handoff.json` contains `schema_version`, `artifact`, `workflows`, safety boundaries, and `handoff_packs` with ticker, company, fiscal period, source freshness, event source, actual source, review status, open review items, thesis note draft, risk map prompts, catalyst follow-up, and evidence artifact hashes when `--visual-receipt` is provided.

`fixture-gallery.json` contains `schema_version`, `artifact`, summary counts, root-level safety boundaries, and `cases` with tickers, event count, stale source labels, high attention scores, post-event availability, supported demo commands, and per-case safety boundaries.

`tutorial-bundle.json` contains `schema_version`, `artifact`, `case_id`, fixture paths, ordered commands, expected artifacts, reviewer checklist, maturity rubric evidence, and safety boundaries.

`showcase.json` contains `schema_version`, `artifact`, title, tagline, value proposition, quickstart commands, demo artifact links, release evidence, maturity rubric, case gallery highlights, tutorial path, risk boundaries, and star-worthy differentiation.

`review-packet-manifest.json` contains `schema_version`, `artifact`, package version, output root, ordered commands, relative artifact paths, artifact roles, media types, byte sizes, SHA-256 hashes, release gate checks, promotion gate notes, risk boundaries, and next review prompts.

`scenario-notebook.json` contains `schema_version`, `artifact`, input artifact names, summary counts, thesis assumptions, scenario bands, source freshness, evidence hashes, comparison aftermath, next-action queue, fixture gallery summary, optional manifests, risk boundary checklist, reusable agent prompts, and safety boundaries.

`portfolio-drift-bridge.json` contains `schema_version`, `artifact`, input artifact names, static threshold values, summary counts, exposure concentration rows, event-linked tickers, scenario mismatch alerts, post-event drift watchlist rows, next risk review prompts, no-trade safety boundaries, and safety boundaries.

`evidence-ledger.json` contains `schema_version`, `artifact`, package version, source manifest paths, git commit metadata when available, release artifact paths, review packet hash inventory, command evidence, maturity rubric mapping, consistency checks, risk boundaries, next evidence requests, and public hygiene flags.

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
