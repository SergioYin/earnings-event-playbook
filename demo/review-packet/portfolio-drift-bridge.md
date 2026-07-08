# Portfolio Drift Bridge

> Local static portfolio drift review packet. No live data, broker connection, order placement, or personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice.

## Summary

- Positions: 2
- Event-linked tickers: 2
- Scenario mismatch alerts: 2
- Post-event drift watchlist: 2
- Total absolute exposure: 25600.00
- Top exposure ticker: EXM

## Thresholds

- `max_position_weight_percent`: 4.0
- `max_exposure_share_percent`: 50.0
- `post_event_move_watch_percent`: 6.0
- `post_event_exposure_drift_amount`: 900.0
- `max_open_review_items`: 6

## Exposure Concentration

| Ticker | Exposure | Weight | Exposure share | Event-linked | Flags |
| --- | ---: | ---: | ---: | --- | --- |
| EXM | 18000.00 | 4.50% | 70.31% | yes | weight-threshold, exposure-share-threshold, event-linked |
| NXT | 7600.00 | 1.90% | 29.69% | yes | event-linked |

## Event-Linked Tickers

| Ticker | Company | Fiscal period | Exposure | Weight | Freshness | Review status |
| --- | --- | --- | ---: | ---: | --- | --- |
| EXM | Example Machines Inc. | FY2026 Q2 | 18000.00 | 4.50% | fresh<=14d | needs-review |
| NXT | Next Retail Group | FY2026 Q1 | 7600.00 | 1.90% | stale>45d | needs-review |

## Scenario Mismatch Alerts

| Ticker | Fiscal period | EPS | Revenue | Move | Review status | Reasons |
| --- | --- | --- | --- | --- | --- | --- |
| EXM | FY2026 Q2 | beat | base | beat | needs-review | eps-revenue-band-divergence, review-status:needs-review |
| NXT | FY2026 Q1 | base | base | miss | needs-review | move-fundamental-band-divergence, review-status:needs-review |

## Post-Event Drift Watchlist

| Ticker | Fiscal period | Actual move | Exposure | Estimated drift | Scenario | Triggers |
| --- | --- | ---: | ---: | ---: | --- | --- |
| EXM | FY2026 Q2 | 7.10% | 18000.00 | 1278.00 | beat | move-threshold, exposure-drift-threshold |
| NXT | FY2026 Q1 | -8.40% | 7600.00 | -638.40 | miss | move-threshold |

## Next Risk Review Prompts

- [ ] Review EXM FY2026 Q2 mismatch reasons before closing the event packet: eps-revenue-band-divergence, review-status:needs-review.
- [ ] Review NXT FY2026 Q1 mismatch reasons before closing the event packet: move-fundamental-band-divergence, review-status:needs-review.
- [ ] Check EXM post-event drift evidence against portfolio exposure and source notes before the next risk review.
- [ ] Check NXT post-event drift evidence against portfolio exposure and source notes before the next risk review.
- [ ] Carry forward EXM risk questions: Did management change full-year guidance assumptions?; Were one-time items separated from recurring demand signals?
- [ ] Carry forward NXT risk questions: Did management change full-year guidance assumptions?; Were one-time items separated from recurring demand signals?
- [ ] Notebook has 9 open review items; triage before the next risk review packet is archived.
- [ ] Open notebook queue item for EXM: Attach actuals source for EXM FY2026 Q2 to the thesis ledger.
- [ ] Open notebook queue item for EXM: EPS and revenue landed in different bands; document which thesis sensitivity changed.
- [ ] Open notebook queue item for EXM: Answer after-call question: Did management change full-year guidance assumptions?
- [ ] Open notebook queue item for EXM: Answer after-call question: Were one-time items separated from recurring demand signals?
- [ ] Open notebook queue item for NXT: Attach actuals source for NXT FY2026 Q1 to the thesis ledger.
- [ ] Open notebook queue item for NXT: Price move scenario differs from fundamentals bands; add market-reaction context.

## No-Trade Safety Boundaries

- Do not treat concentration flags as trade instructions.
- Do not convert scenario mismatch alerts into buy, sell, hold, hedge, rebalance, or allocation actions.
- Do not place, route, stage, or simulate orders from this packet.
- Do not use this packet without independent source review and suitability review outside this package.

## Safety Boundaries

- local static fixtures and generated artifacts only
- no live market data
- no broker connection
- no order placement
- no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice
- descriptive portfolio drift review only
