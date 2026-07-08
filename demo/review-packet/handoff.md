# Cross-Asset Handoff Pack

> Educational research handoff only. Local static artifacts only; no live data, broker connection, orders, or investment advice.

## Summary

- Handoff packs: 2
- Open review items: 9
- Evidence hashes attached: 30

## Workflows

- thesis-ledger
- earnings-call-risk-map

## EXM - Example Machines Inc.

- Fiscal period: FY2026 Q2
- Source freshness: fresh<=14d
- Event source: Static consensus fixture (2026-07-05)
- Actuals source: Static post-event fixture (2026-07-24)
- Review status: needs-review

### Thesis Note Draft

EXM FY2026 Q2 handoff: review status needs-review. EPS band beat; revenue band base; post-event move matched beat. Pre-event source freshness was fresh<=14d; actuals source was Static post-event fixture. Use this as a thesis-ledger draft note after source review; it is not an action recommendation.

### Open Review Items

- Attach actuals source for EXM FY2026 Q2 to the thesis ledger.
- EPS and revenue landed in different bands; document which thesis sensitivity changed.
- Answer after-call question: Did management change full-year guidance assumptions?
- Answer after-call question: Were one-time items separated from recurring demand signals?

### Risk Map Prompts

- Map EXM FY2026 Q2 source freshness (fresh<=14d) to the call-risk log.
- Identify which thesis sensitivities need updated evidence after the earnings call.
- Call-risk prompt: Did management change full-year guidance assumptions?
- Call-risk prompt: Were one-time items separated from recurring demand signals?
- Compare EPS band beat, revenue band base, and move scenario beat for divergence.

### Catalyst Follow-Up

- Carry forward unresolved EXM FY2026 Q2 review items into the next catalyst log.
- Attach source artifacts and notes before marking the event review closed.
- Review actuals note for catalyst context: Revenue and margin comments require ledger follow-up against pre-event sensitivities.
- Update thesis sensitivity evidence for: gross margin, demand durability.

### Evidence Artifact Hashes

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
| `review-packet/review-packet-manifest.json` | json-artifact | 13198 | `111d32cffec8267667d431ac18edd8fd965ab271145a126576df3aa937f428eb` |
| `review-packet/showcase.html` | html-artifact | 10879 | `8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca` |
| `review-packet/showcase.json` | json-artifact | 7351 | `e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a` |
| `review-packet/tutorial-bundle.json` | json-artifact | 4938 | `43fe3db28198add8399d23a5898b5393cb9510ec1209a81a177b53b8655a8c47` |
| `review-packet/tutorial-bundle.md` | markdown-artifact | 4236 | `d22f4698d14eaffe4e69dc148466c2d1d5d47166c282beeca50a101e734e30a1` |

## NXT - Next Retail Group

- Fiscal period: FY2026 Q1
- Source freshness: stale>45d
- Event source: Static calendar fixture (2026-05-12)
- Actuals source: Static post-event fixture (2026-08-01)
- Review status: needs-review

### Thesis Note Draft

NXT FY2026 Q1 handoff: review status needs-review. EPS band base; revenue band base; post-event move matched miss. Pre-event source freshness was stale>45d; actuals source was Static post-event fixture. Use this as a thesis-ledger draft note after source review; it is not an action recommendation.

### Open Review Items

- Attach actuals source for NXT FY2026 Q1 to the thesis ledger.
- Price move scenario differs from fundamentals bands; add market-reaction context.
- Answer after-call question: Did management change full-year guidance assumptions?
- Answer after-call question: Were one-time items separated from recurring demand signals?
- Refresh source freshness for NXT before closing handoff.

### Risk Map Prompts

- Map NXT FY2026 Q1 source freshness (stale>45d) to the call-risk log.
- Identify which thesis sensitivities need updated evidence after the earnings call.
- Call-risk prompt: Did management change full-year guidance assumptions?
- Call-risk prompt: Were one-time items separated from recurring demand signals?
- Compare EPS band base, revenue band base, and move scenario miss for divergence.

### Catalyst Follow-Up

- Carry forward unresolved NXT FY2026 Q1 review items into the next catalyst log.
- Attach source artifacts and notes before marking the event review closed.
- Review actuals note for catalyst context: Management commentary should be attached before closing the review queue.
- Update thesis sensitivity evidence for: gross margin, demand durability.

### Evidence Artifact Hashes

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
| `review-packet/review-packet-manifest.json` | json-artifact | 13198 | `111d32cffec8267667d431ac18edd8fd965ab271145a126576df3aa937f428eb` |
| `review-packet/showcase.html` | html-artifact | 10879 | `8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca` |
| `review-packet/showcase.json` | json-artifact | 7351 | `e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a` |
| `review-packet/tutorial-bundle.json` | json-artifact | 4938 | `43fe3db28198add8399d23a5898b5393cb9510ec1209a81a177b53b8655a8c47` |
| `review-packet/tutorial-bundle.md` | markdown-artifact | 4236 | `d22f4698d14eaffe4e69dc148466c2d1d5d47166c282beeca50a101e734e30a1` |
