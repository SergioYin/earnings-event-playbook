# Scenario Reviewer Notebook

> Local static reviewer notebook. No live data, broker connection, orders, or personalized investment, legal, tax, accounting, buy, sell, hold, or allocation advice.

## Summary

- Playbooks: 2
- Handoff packs: 2
- Fixture cases: 3
- Optional manifests: 1
- Open review items: 9
- Evidence hashes: 24

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
| EXM, NXT | `demo/actuals.json` | input-fixture | 810 | `d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79` |
| EXM, NXT | `demo/cases/retail/playbook.json` | playbook-json | 9147 | `78cb5e6b591e764b6c9f9dd9e64acaf1345e54620f1cd5243a6e47d040917571` |
| EXM, NXT | `demo/cases/retail/playbook.md` | playbook-markdown | 4187 | `b3b0c1af8af86678541eccf62634ff2901948e8e9f5b2e779f24fe9f37068e52` |
| EXM, NXT | `demo/cases/semiconductor/playbook.json` | playbook-json | 6420 | `9c0c42158b3da6d4fc346a876028ea7393c104c833b530a1c938197a415a5e69` |
| EXM, NXT | `demo/cases/semiconductor/playbook.md` | playbook-markdown | 3003 | `5ba36bc34a19570bd8e04f545649e2b0596953da81fe01ece1bb025bdf874d46` |
| EXM, NXT | `demo/cases/semiconductor/post-event-compare.json` | post-event-json | 4173 | `06035cbe0d994fb5cb454af738fe395275a789b60d314bb98ae9783d9ff9d156` |
| EXM, NXT | `demo/cases/semiconductor/post-event-compare.md` | post-event-markdown | 2423 | `f22106635dd8d70908d3cacf8b76adb22c923a8069b578581a542cde4eedcc82` |
| EXM, NXT | `demo/cases/software/playbook.json` | playbook-json | 6557 | `285e03d8221afbe224ec8a089144417717378a26d7f8a271a8df9f4c87c1dbf9` |
| EXM, NXT | `demo/cases/software/playbook.md` | playbook-markdown | 3131 | `829fea4fe415e3ee0b075489e1916c193b55da08e6fad02a11dd29bc6604d093` |
| EXM, NXT | `demo/cases/software/post-event-compare.json` | post-event-json | 5186 | `b5f98980982b8f653844e08816803ab6773b01dc696fbd3ea7fdd4df901684a8` |
| EXM, NXT | `demo/cases/software/post-event-compare.md` | post-event-markdown | 3097 | `107cdaafe21a4260e8bce5380c7ca031af8f3a3a608395255cfacf1313c2fa22` |
| EXM, NXT | `demo/events.json` | input-fixture | 1211 | `972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc` |
| EXM, NXT | `demo/fixture-gallery.json` | json-artifact | 4139 | `3965bf845ee22791be53507c37fe709cebc83111960b10b6614144a1a6c8c35d` |
| EXM, NXT | `demo/fixture-gallery.md` | markdown-artifact | 2308 | `85245a266cacca9861b74e9b9fa097f0982c97bcfebbf140b0fa55326d81f607` |
| EXM, NXT | `demo/index.html` | static-html-preview | 4028 | `2e61b1da39ce3fbd6b67f66141a71de9c1995546f2bdf310c081e3a89dec735b` |
| EXM, NXT | `demo/playbook.json` | playbook-json | 6263 | `3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34` |
| EXM, NXT | `demo/playbook.md` | playbook-markdown | 2856 | `59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47` |
| EXM, NXT | `demo/portfolio.json` | input-fixture | 442 | `552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00` |
| EXM, NXT | `demo/post-event-compare.json` | post-event-json | 5099 | `72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79` |
| EXM, NXT | `demo/post-event-compare.md` | post-event-markdown | 3035 | `a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb` |
| EXM, NXT | `demo/showcase.html` | html-artifact | 9851 | `e32783a6885a5121d82dd4c1ef2cc047b65a3cbae93dd5451dc35f9d83acc587` |
| EXM, NXT | `demo/showcase.json` | json-artifact | 6356 | `7a203f7bddeeb1c3a21df3c8c1de9f8c7273742244a879e80c54449fee34e8dd` |
| EXM, NXT | `demo/tutorial-bundle.json` | json-artifact | 4704 | `08b39909a94d0b96c347f5b60186681c9a892644177eb230683c0e4786fb6b63` |
| EXM, NXT | `demo/tutorial-bundle.md` | markdown-artifact | 4002 | `7f5cd3d252e0ec61bfe07762f023bed72dc029200fd9ac461e33dc74170aedfc` |

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

- `showcase-page`: Earnings Event Playbook Showcase (11 paths/commands)

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
