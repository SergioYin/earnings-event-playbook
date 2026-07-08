# Scenario Reviewer Notebook

> Local static reviewer notebook. No live data, broker connection, orders, or personalized investment, legal, tax, accounting, buy, sell, hold, or allocation advice.

## Summary

- Playbooks: 2
- Handoff packs: 2
- Fixture cases: 3
- Optional manifests: 2
- Open review items: 9
- Evidence hashes: 15

## Thesis Assumptions

### EXM - Example Machines Inc.

- Fiscal period: FY2026 Q2
- Attention score: 46
- Position exposure: 18000.00
- Portfolio weight: 4.50%
- Sensitivity: gross margin (3): Margin guide and inventory commentary can change confidence in the near-term thesis.
- Sensitivity: demand durability (2): Backlog quality and repeat-order language should be reviewed after the call.
- Risk question: Did management change full-year guidance assumptions?
- Risk question: Were one-time items separated from recurring demand signals?

### NXT - Next Retail Group

- Fiscal period: FY2026 Q1
- Attention score: 48
- Position exposure: 7600.00
- Portfolio weight: 1.90%
- Sensitivity: gross margin (3): Margin guide and inventory commentary can change confidence in the near-term thesis.
- Sensitivity: demand durability (2): Backlog quality and repeat-order language should be reviewed after the call.
- Risk question: Did management change full-year guidance assumptions?
- Risk question: Were one-time items separated from recurring demand signals?

## Scenario Bands

### EXM FY2026 Q2

| Band | Price move | EPS delta | Revenue delta | Exposure delta | Watch items |
| --- | ---: | ---: | ---: | ---: | --- |
| beat | 6.50% | 8.00% | 5.00% | 1170.00 | compare actual EPS to consensus; compare actual revenue to consensus; check guidance tone before changing thesis notes |
| base | 0.00% | 0.00% | 0.00% | 0.00 | compare actual EPS to consensus; compare actual revenue to consensus; check guidance tone before changing thesis notes |
| miss | -6.50% | -8.00% | -5.00% | -1170.00 | compare actual EPS to consensus; compare actual revenue to consensus; check guidance tone before changing thesis notes |

### NXT FY2026 Q1

| Band | Price move | EPS delta | Revenue delta | Exposure delta | Watch items |
| --- | ---: | ---: | ---: | ---: | --- |
| beat | 9.20% | 8.00% | 5.00% | 699.20 | compare actual EPS to consensus; compare actual revenue to consensus; check guidance tone before changing thesis notes |
| base | 0.00% | 0.00% | 0.00% | 0.00 | compare actual EPS to consensus; compare actual revenue to consensus; check guidance tone before changing thesis notes |
| miss | -9.20% | -8.00% | -5.00% | -699.20 | compare actual EPS to consensus; compare actual revenue to consensus; check guidance tone before changing thesis notes |

## Source Freshness

| Ticker | Fiscal period | Event source | Freshness | Handoff status |
| --- | --- | --- | --- | --- |
| EXM | FY2026 Q2 | Static consensus fixture (2026-07-05) | fresh<=14d | needs-review |
| NXT | FY2026 Q1 | Static calendar fixture (2026-05-12) | stale>45d | needs-review |

## Evidence Hashes

| Ticker | Path | Role | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| EXM, NXT | `review-packet/fixture-gallery.json` | json-artifact | 4139 | `3965bf845ee22791be53507c37fe709cebc83111960b10b6614144a1a6c8c35d` |
| EXM, NXT | `review-packet/fixture-gallery.md` | markdown-artifact | 2308 | `85245a266cacca9861b74e9b9fa097f0982c97bcfebbf140b0fa55326d81f607` |
| EXM, NXT | `review-packet/inputs/actuals.json` | input-fixture | 810 | `d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79` |
| EXM, NXT | `review-packet/inputs/events.json` | input-fixture | 1211 | `972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc` |
| EXM, NXT | `review-packet/inputs/portfolio.json` | input-fixture | 442 | `552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00` |
| EXM, NXT | `review-packet/inputs/risk-thresholds.json` | json-artifact | 591 | `eb05108dbc8bde62cfe54b9a3e4688711ab1c5eb60c7e8b320695aecd9a8bc42` |
| EXM, NXT | `review-packet/playbook.json` | playbook-json | 6263 | `3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34` |
| EXM, NXT | `review-packet/playbook.md` | playbook-markdown | 2856 | `59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47` |
| EXM, NXT | `review-packet/post-event-compare.json` | post-event-json | 5099 | `72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79` |
| EXM, NXT | `review-packet/post-event-compare.md` | post-event-markdown | 3035 | `a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb` |
| EXM, NXT | `review-packet/review-packet-manifest.json` | json-artifact | 13198 | `111d32cffec8267667d431ac18edd8fd965ab271145a126576df3aa937f428eb` |
| EXM, NXT | `review-packet/showcase.html` | html-artifact | 10879 | `8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca` |
| EXM, NXT | `review-packet/showcase.json` | json-artifact | 7351 | `e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a` |
| EXM, NXT | `review-packet/tutorial-bundle.json` | json-artifact | 4938 | `43fe3db28198add8399d23a5898b5393cb9510ec1209a81a177b53b8655a8c47` |
| EXM, NXT | `review-packet/tutorial-bundle.md` | markdown-artifact | 4236 | `d22f4698d14eaffe4e69dc148466c2d1d5d47166c282beeca50a101e734e30a1` |

## Comparison Aftermath

### EXM FY2026 Q2

- Review status: `needs-review`
- Thesis note draft: EXM FY2026 Q2 handoff: review status needs-review. EPS band beat; revenue band base; post-event move matched beat. Pre-event source freshness was fresh<=14d; actuals source was Static post-event fixture. Use this as a thesis-ledger draft note after source review; it is not an action recommendation.
- Catalyst follow-up: Carry forward unresolved EXM FY2026 Q2 review items into the next catalyst log.
- Catalyst follow-up: Attach source artifacts and notes before marking the event review closed.
- Catalyst follow-up: Review actuals note for catalyst context: Revenue and margin comments require ledger follow-up against pre-event sensitivities.
- Catalyst follow-up: Update thesis sensitivity evidence for: gross margin, demand durability.

### NXT FY2026 Q1

- Review status: `needs-review`
- Thesis note draft: NXT FY2026 Q1 handoff: review status needs-review. EPS band base; revenue band base; post-event move matched miss. Pre-event source freshness was stale>45d; actuals source was Static post-event fixture. Use this as a thesis-ledger draft note after source review; it is not an action recommendation.
- Catalyst follow-up: Carry forward unresolved NXT FY2026 Q1 review items into the next catalyst log.
- Catalyst follow-up: Attach source artifacts and notes before marking the event review closed.
- Catalyst follow-up: Review actuals note for catalyst context: Management commentary should be attached before closing the review queue.
- Catalyst follow-up: Update thesis sensitivity evidence for: gross margin, demand durability.

## Next-Action Queue

- [ ] EXM FY2026 Q2: Attach actuals source for EXM FY2026 Q2 to the thesis ledger.
- [ ] EXM FY2026 Q2: EPS and revenue landed in different bands; document which thesis sensitivity changed.
- [ ] EXM FY2026 Q2: Answer after-call question: Did management change full-year guidance assumptions?
- [ ] EXM FY2026 Q2: Answer after-call question: Were one-time items separated from recurring demand signals?
- [ ] NXT FY2026 Q1: Attach actuals source for NXT FY2026 Q1 to the thesis ledger.
- [ ] NXT FY2026 Q1: Price move scenario differs from fundamentals bands; add market-reaction context.
- [ ] NXT FY2026 Q1: Answer after-call question: Did management change full-year guidance assumptions?
- [ ] NXT FY2026 Q1: Answer after-call question: Were one-time items separated from recurring demand signals?
- [ ] NXT FY2026 Q1: Refresh source freshness for NXT before closing handoff.

## Fixture Gallery Snapshot

- `retail`: 3 events, tickers FASH, GROC, HOME, post-event 0 matched
- `semiconductor`: 2 events, tickers AICH, MEMR, post-event 1 matched
- `software`: 2 events, tickers CLDW, SECX, post-event 2 matched

## Optional Manifest Snapshot

- `tutorial-bundle`: tutorial-bundle (5 paths/commands)
- `showcase-page`: Earnings Event Playbook Showcase (12 paths/commands)

## Risk Boundary Checklist

- [ ] Confirm every source date is acceptable for the review window.
- [ ] Confirm scenario bands are treated as deterministic fixture calculations, not forecasts.
- [ ] Confirm handoff packs have matching playbook tickers and fiscal periods.
- [ ] Confirm evidence hashes point to local generated artifacts.
- [ ] Confirm optional tutorial and showcase manifests reference local public paths only.
- [ ] Confirm unresolved review queue items stay open until source materials are attached.

## Reusable Agent Prompts

### thesis ledger updater

Using the scenario notebook JSON, draft concise thesis-ledger notes grouped by ticker, source freshness, scenario band, review status, open queue item, and evidence hash. Keep the output descriptive and do not include action language.

### earnings call risk mapper

Using the scenario notebook JSON, convert risk questions and handoff prompts into an earnings-call risk map with source freshness, unresolved assumptions, and follow-up evidence fields.

### release reviewer

Using the scenario notebook JSON, verify artifact completeness, local-only boundaries, evidence hashes, optional manifests, and open review items before release.

## Safety Boundaries

- local static artifacts only
- no live market data
- no broker connection
- no order placement
- no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice
- descriptive reviewer notebook only
