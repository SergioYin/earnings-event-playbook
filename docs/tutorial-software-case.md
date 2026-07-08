# Software Case Tutorial

This tutorial walks the checked-in software case from static fixtures to a playbook, post-event compare, visual receipt, handoff pack, and fixture gallery.

It is an educational research review workflow. It uses local static files only. It does not fetch live data, connect to brokers, place orders, or provide personalized investment, legal, tax, accounting, buy, sell, or hold advice.

## 1. Start With Static Fixtures

The software case lives under `examples/cases/software`.

- `events.json` contains two synthetic software earnings events: `CLDW` and `SECX`.
- `portfolio.json` contains matching local position context.
- `actuals.json` contains post-event actual EPS, revenue, move, source, and notes.

Review these files first because every downstream artifact is deterministic from them.

## 2. Build The Playbook

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/cases/software/events.json --portfolio examples/cases/software/portfolio.json --out demo/cases/software/playbook.md --json-out demo/cases/software/playbook.json
```

Expected artifacts:

- `demo/cases/software/playbook.md`
- `demo/cases/software/playbook.json`

The playbook captures event date, fiscal period, consensus fields, implied move, source freshness, attention score, position context, scenario bands, thesis sensitivities, risk questions, and post-event review queue items.

## 3. Compare Post-Event Actuals

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/cases/software/playbook.json --actuals examples/cases/software/actuals.json --out demo/cases/software/post-event-compare.md --json-out demo/cases/software/post-event-compare.json
```

Expected artifacts:

- `demo/cases/software/post-event-compare.md`
- `demo/cases/software/post-event-compare.json`

The compare artifact matches actual EPS, revenue, and post-event move against the pre-event playbook. It records matched scenario bands, review status, thesis-ledger handoff notes, and remaining review queue items. It describes what changed; it does not recommend an action.

## 4. Create A Visual Receipt

```bash
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo/cases/software --out demo/cases/software/visual-receipt.md --json-out demo/cases/software/visual-receipt.json
```

Expected artifacts:

- `demo/cases/software/visual-receipt.md`
- `demo/cases/software/visual-receipt.json`

The receipt scans local Markdown and JSON artifacts, assigns file roles, and records byte sizes and SHA-256 hashes. Receipt and handoff outputs are excluded from receipt inventory to avoid circular evidence.

## 5. Export The Handoff

```bash
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/cases/software/playbook.json --post-event-compare demo/cases/software/post-event-compare.json --visual-receipt demo/cases/software/visual-receipt.json --out demo/cases/software/handoff.md --json-out demo/cases/software/handoff.json
```

Expected artifacts:

- `demo/cases/software/handoff.md`
- `demo/cases/software/handoff.json`

The handoff pack carries ticker, company, fiscal period, source freshness, review status, open review items, thesis-note draft language, risk-map prompts, catalyst follow-up, and optional evidence hashes from the receipt. It is meant for a local thesis ledger or earnings-call risk map.

## 6. Refresh The Fixture Gallery

```bash
PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out demo/fixture-gallery.md --json-out demo/fixture-gallery.json
```

Expected artifacts:

- `demo/fixture-gallery.md`
- `demo/fixture-gallery.json`

The gallery compares local case coverage across software, retail, and semiconductor fixtures. It summarizes tickers, event counts, stale-source labels, high-attention scores, post-event availability, and supported demo commands.

## 7. Generate The Tutorial Packet

```bash
PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json
```

Expected artifacts:

- `demo/tutorial-bundle.md`
- `demo/tutorial-bundle.json`

The tutorial bundle is a deterministic reviewer packet. It lists the ordered commands above, expected artifact paths, reviewer checklist, maturity rubric evidence, and safety boundaries in both Markdown and JSON.

## Reviewer Checklist

- Confirm the fixture files are local, static, and synthetic.
- Confirm Markdown and JSON artifacts agree on tickers, fiscal periods, review statuses, and expected output paths.
- Confirm visual receipt hashes are regenerated from local artifacts.
- Confirm handoff packs include open review items and evidence references without action recommendations.
- Confirm the fixture gallery includes the software case and shows post-event actuals availability.
- Confirm safety language remains present in generated artifacts and docs.
