# Visual Evidence Receipt

> Deterministic receipt for local demo artifacts. Static files only; no live data, broker connection, orders, or recommendations.

## Summary

- Artifact root: `demo`
- Files scanned: 8
- Total bytes: 23744

## File Roles

- input-fixture: 3
- playbook-json: 1
- playbook-markdown: 1
- post-event-json: 1
- post-event-markdown: 1
- static-html-preview: 1

## Artifact Inventory

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `demo/actuals.json` | input-fixture | 810 | `d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79` |
| `demo/events.json` | input-fixture | 1211 | `972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc` |
| `demo/index.html` | static-html-preview | 4028 | `2e61b1da39ce3fbd6b67f66141a71de9c1995546f2bdf310c081e3a89dec735b` |
| `demo/playbook.json` | playbook-json | 6263 | `3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34` |
| `demo/playbook.md` | playbook-markdown | 2856 | `59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47` |
| `demo/portfolio.json` | input-fixture | 442 | `552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00` |
| `demo/post-event-compare.json` | post-event-json | 5099 | `72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79` |
| `demo/post-event-compare.md` | post-event-markdown | 3035 | `a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb` |

## Regeneration Commands

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
```

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
```

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
```

```bash
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
```

```bash
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
```

## Review Checklist

- [ ] Open demo/index.html directly in a browser and confirm the static preview renders.
- [ ] Review demo/playbook.md for event fields, scenario bands, risk questions, and review queue items.
- [ ] Review demo/post-event-compare.md for actuals comparisons, matched scenarios, and ledger handoff notes.
- [ ] Compare JSON artifacts against Markdown outputs for matching tickers, periods, and review counts.
- [ ] Confirm receipt hashes after regenerating the demo artifacts.

## Safety Boundaries

- local static artifacts only
- no live market data
- no broker connection
- no order placement
- no personalized investment advice
