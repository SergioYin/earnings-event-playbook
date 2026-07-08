# Visual Evidence Receipt

> Deterministic receipt for local demo artifacts. Static files only; no live data, broker connection, orders, or recommendations.

## Summary

- Artifact root: `demo`
- Files scanned: 24
- Total bytes: 104451

## File Roles

- html-artifact: 1
- input-fixture: 3
- json-artifact: 3
- markdown-artifact: 2
- playbook-json: 4
- playbook-markdown: 4
- post-event-json: 3
- post-event-markdown: 3
- static-html-preview: 1

## Artifact Inventory

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `demo/actuals.json` | input-fixture | 810 | `d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79` |
| `demo/cases/retail/playbook.json` | playbook-json | 9147 | `78cb5e6b591e764b6c9f9dd9e64acaf1345e54620f1cd5243a6e47d040917571` |
| `demo/cases/retail/playbook.md` | playbook-markdown | 4187 | `b3b0c1af8af86678541eccf62634ff2901948e8e9f5b2e779f24fe9f37068e52` |
| `demo/cases/semiconductor/playbook.json` | playbook-json | 6420 | `9c0c42158b3da6d4fc346a876028ea7393c104c833b530a1c938197a415a5e69` |
| `demo/cases/semiconductor/playbook.md` | playbook-markdown | 3003 | `5ba36bc34a19570bd8e04f545649e2b0596953da81fe01ece1bb025bdf874d46` |
| `demo/cases/semiconductor/post-event-compare.json` | post-event-json | 4173 | `06035cbe0d994fb5cb454af738fe395275a789b60d314bb98ae9783d9ff9d156` |
| `demo/cases/semiconductor/post-event-compare.md` | post-event-markdown | 2423 | `f22106635dd8d70908d3cacf8b76adb22c923a8069b578581a542cde4eedcc82` |
| `demo/cases/software/playbook.json` | playbook-json | 6557 | `285e03d8221afbe224ec8a089144417717378a26d7f8a271a8df9f4c87c1dbf9` |
| `demo/cases/software/playbook.md` | playbook-markdown | 3131 | `829fea4fe415e3ee0b075489e1916c193b55da08e6fad02a11dd29bc6604d093` |
| `demo/cases/software/post-event-compare.json` | post-event-json | 5186 | `b5f98980982b8f653844e08816803ab6773b01dc696fbd3ea7fdd4df901684a8` |
| `demo/cases/software/post-event-compare.md` | post-event-markdown | 3097 | `107cdaafe21a4260e8bce5380c7ca031af8f3a3a608395255cfacf1313c2fa22` |
| `demo/events.json` | input-fixture | 1211 | `972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc` |
| `demo/fixture-gallery.json` | json-artifact | 4139 | `3965bf845ee22791be53507c37fe709cebc83111960b10b6614144a1a6c8c35d` |
| `demo/fixture-gallery.md` | markdown-artifact | 2308 | `85245a266cacca9861b74e9b9fa097f0982c97bcfebbf140b0fa55326d81f607` |
| `demo/index.html` | static-html-preview | 4028 | `2e61b1da39ce3fbd6b67f66141a71de9c1995546f2bdf310c081e3a89dec735b` |
| `demo/playbook.json` | playbook-json | 6263 | `3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34` |
| `demo/playbook.md` | playbook-markdown | 2856 | `59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47` |
| `demo/portfolio.json` | input-fixture | 442 | `552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00` |
| `demo/post-event-compare.json` | post-event-json | 5099 | `72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79` |
| `demo/post-event-compare.md` | post-event-markdown | 3035 | `a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb` |
| `demo/showcase.html` | html-artifact | 10879 | `8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca` |
| `demo/showcase.json` | json-artifact | 7351 | `e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a` |
| `demo/tutorial-bundle.json` | json-artifact | 4704 | `08b39909a94d0b96c347f5b60186681c9a892644177eb230683c0e4786fb6b63` |
| `demo/tutorial-bundle.md` | markdown-artifact | 4002 | `7f5cd3d252e0ec61bfe07762f023bed72dc029200fd9ac461e33dc74170aedfc` |

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
