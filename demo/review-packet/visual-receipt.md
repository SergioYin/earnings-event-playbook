# Visual Evidence Receipt

> Deterministic receipt for local demo artifacts. Static files only; no live data, broker connection, orders, or recommendations.

## Summary

- Artifact root: `review-packet`
- Files scanned: 14
- Total bytes: 54158

## File Roles

- html-artifact: 1
- input-fixture: 3
- json-artifact: 4
- markdown-artifact: 2
- playbook-json: 1
- playbook-markdown: 1
- post-event-json: 1
- post-event-markdown: 1

## Artifact Inventory

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `review-packet/fixture-gallery.json` | json-artifact | 4139 | `3965bf845ee22791be53507c37fe709cebc83111960b10b6614144a1a6c8c35d` |
| `review-packet/fixture-gallery.md` | markdown-artifact | 2308 | `85245a266cacca9861b74e9b9fa097f0982c97bcfebbf140b0fa55326d81f607` |
| `review-packet/inputs/actuals.json` | input-fixture | 810 | `d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79` |
| `review-packet/inputs/events.json` | input-fixture | 1211 | `972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc` |
| `review-packet/inputs/portfolio.json` | input-fixture | 442 | `552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00` |
| `review-packet/inputs/risk-thresholds.json` | json-artifact | 591 | `eb05108dbc8bde62cfe54b9a3e4688711ab1c5eb60c7e8b320695aecd9a8bc42` |
| `review-packet/playbook.json` | playbook-json | 6263 | `3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34` |
| `review-packet/playbook.md` | playbook-markdown | 2856 | `59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47` |
| `review-packet/post-event-compare.json` | post-event-json | 5099 | `72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79` |
| `review-packet/post-event-compare.md` | post-event-markdown | 3035 | `a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb` |
| `review-packet/showcase.html` | html-artifact | 10879 | `8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca` |
| `review-packet/showcase.json` | json-artifact | 7351 | `e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a` |
| `review-packet/tutorial-bundle.json` | json-artifact | 4938 | `43fe3db28198add8399d23a5898b5393cb9510ec1209a81a177b53b8655a8c47` |
| `review-packet/tutorial-bundle.md` | markdown-artifact | 4236 | `d22f4698d14eaffe4e69dc148466c2d1d5d47166c282beeca50a101e734e30a1` |

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
PYTHONPATH=src python -m earnings_event_playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json
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
