# Fixture Case Gallery

> Educational fixture comparison only. Local static fixtures only; no live data, broker connection, orders, or investment advice.

## Summary

- Cases: 3
- Events: 7
- Tickers: AICH, CLDW, FASH, GROC, HOME, MEMR, SECX
- Stale source flags: 3
- High attention flags: 3
- Cases with post-event actuals: 2

## Case Comparison

| Case | Tickers | Events | Stale sources | High attention | Post-event availability |
| --- | --- | ---: | --- | --- | --- |
| `retail` | FASH, GROC, HOME | 3 | GROC:stale>45d | None | No actuals fixture |
| `semiconductor` | AICH, MEMR | 2 | MEMR:stale>45d | AICH 70, MEMR 70 | 1/2 matched |
| `software` | CLDW, SECX | 2 | SECX:stale>45d | SECX 71 | 2/2 matched |

## Supported Demo Commands

### retail

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/cases/retail/events.json --portfolio examples/cases/retail/portfolio.json --out demo/cases/retail/playbook.md --json-out demo/cases/retail/playbook.json
```

### semiconductor

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/cases/semiconductor/events.json --portfolio examples/cases/semiconductor/portfolio.json --out demo/cases/semiconductor/playbook.md --json-out demo/cases/semiconductor/playbook.json
```

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/cases/semiconductor/playbook.json --actuals examples/cases/semiconductor/actuals.json --out demo/cases/semiconductor/post-event-compare.md --json-out demo/cases/semiconductor/post-event-compare.json
```

### software

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/cases/software/events.json --portfolio examples/cases/software/portfolio.json --out demo/cases/software/playbook.md --json-out demo/cases/software/playbook.json
```

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/cases/software/playbook.json --actuals examples/cases/software/actuals.json --out demo/cases/software/post-event-compare.md --json-out demo/cases/software/post-event-compare.json
```

## Safety Boundaries

- local static fixtures only
- no live market data
- no broker connection
- no order placement
- no personalized investment advice
