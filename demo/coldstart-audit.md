# Cold-Start Audit

- Package version: `1.3.0`
- Manifest: `demo/review-packet/review-packet-manifest.json`
- Score: 100/100 (pass)
- Promotion summary: Ready to promote after all blockers are cleared.

## Readiness Score

| Dimension | Score | Evidence |
| --- | ---: | --- |
| clone | 20/20 | package_version=1.3.0; quickstart_commands=14 |
| read | 20/20 | 7/7 required documents complete |
| run | 20/20 | 14 exact README quickstart commands; 6/6 release gates pass |
| trust | 20/20 | 22/22 manifest artifacts exist and match SHA-256 |
| promote | 20/20 | no promotion blockers |

## Missing-Doc Checks

| Path | Status | Missing Terms |
| --- | --- | --- |
| `README.md` | pass | none |
| `docs/usage.md` | pass | none |
| `docs/review-packet.md` | pass | none |
| `docs/release-readiness.md` | pass | none |
| `docs/promote.md` | pass | none |
| `docs/coldstart-audit.md` | pass | none |
| `demo/review-packet/review-packet-manifest.json` | pass | none |

## Exact Quickstart Commands

- `PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json`
- `PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json`
- `PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json`
- `PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo`
- `PYTHONPATH=src python -m earnings_event_playbook evidence-ledger --release-manifest release_manifest.json --review-manifest demo/review-packet/review-packet-manifest.json --coldstart-audit demo/coldstart-audit.json --out demo/evidence-ledger.md --json-out demo/evidence-ledger.json`
- `PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json`
- `PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out demo/fixture-gallery.md --json-out demo/fixture-gallery.json`
- `PYTHONPATH=src python -m earnings_event_playbook portfolio-drift-bridge --portfolio examples/portfolio.json --scenario-notebook demo/scenario-notebook.json --post-event-compare demo/post-event-compare.json --risk-thresholds examples/risk-thresholds.json --out demo/portfolio-drift-bridge.md --json-out demo/portfolio-drift-bridge.json`
- `PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet`
- `PYTHONPATH=src python -m earnings_event_playbook scenario-notebook --playbook demo/playbook.json --handoff demo/handoff.json --fixture-gallery demo/fixture-gallery.json --manifest demo/tutorial-bundle.json demo/showcase.json --out demo/scenario-notebook.md --json-out demo/scenario-notebook.json`
- `PYTHONPATH=src python -m earnings_event_playbook selfcheck`
- `PYTHONPATH=src python -m earnings_event_playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json`
- `PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json`
- `PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json`

## Artifact Existence And Hash Checks

| Path | Role | Status | SHA-256 |
| --- | --- | --- | --- |
| `review-packet/fixture-gallery.json` | case-gallery-artifact | pass | 3965bf845ee22791be53507c37fe709cebc83111960b10b6614144a1a6c8c35d |
| `review-packet/fixture-gallery.md` | case-gallery-artifact | pass | 85245a266cacca9861b74e9b9fa097f0982c97bcfebbf140b0fa55326d81f607 |
| `review-packet/handoff.json` | cross-asset-handoff-artifact | pass | c33ea4601a0a4f99a023ebc3e0acb71b72105fc66449b0b92b14007ba25ea943 |
| `review-packet/handoff.md` | cross-asset-handoff-artifact | pass | ae6d279706623d71f315debcb1ef9c123212a10c39769e4f637674920cfe0fcb |
| `review-packet/inputs/actuals.json` | input-fixture | pass | d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79 |
| `review-packet/inputs/events.json` | input-fixture | pass | 972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc |
| `review-packet/inputs/portfolio.json` | input-fixture | pass | 552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00 |
| `review-packet/inputs/risk-thresholds.json` | input-fixture | pass | eb05108dbc8bde62cfe54b9a3e4688711ab1c5eb60c7e8b320695aecd9a8bc42 |
| `review-packet/playbook.json` | pre-event-playbook-artifact | pass | 3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34 |
| `review-packet/playbook.md` | pre-event-playbook-artifact | pass | 59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47 |
| `review-packet/portfolio-drift-bridge.json` | portfolio-drift-artifact | pass | bc3fa072331df1af64c68360473e114b9891f244f928c00425b3cd7bde3a7f4f |
| `review-packet/portfolio-drift-bridge.md` | portfolio-drift-artifact | pass | 10436cd2b6083ef9df49df701139956996e7d35b0db3982646ec174b4a3478d0 |
| `review-packet/post-event-compare.json` | post-event-comparison-artifact | pass | 72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79 |
| `review-packet/post-event-compare.md` | post-event-comparison-artifact | pass | a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb |
| `review-packet/scenario-notebook.json` | scenario-review-artifact | pass | c54299867c4139c3b8cde479c8e7a7fb9b3495f5af9db6f5c41bc17f30aa16c2 |
| `review-packet/scenario-notebook.md` | scenario-review-artifact | pass | 334c90b2ad744543596931838d58c86ea241490d18f715aa7f7a6eb2ca9ade33 |
| `review-packet/showcase.html` | showcase-artifact | pass | 8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca |
| `review-packet/showcase.json` | showcase-artifact | pass | e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a |
| `review-packet/tutorial-bundle.json` | tutorial-artifact | pass | 43fe3db28198add8399d23a5898b5393cb9510ec1209a81a177b53b8655a8c47 |
| `review-packet/tutorial-bundle.md` | tutorial-artifact | pass | d22f4698d14eaffe4e69dc148466c2d1d5d47166c282beeca50a101e734e30a1 |
| `review-packet/visual-receipt.json` | hash-receipt-artifact | pass | 66bb64e5364745eda38e902833faad8a7b1fc894711bdb85940e7dfc3433a1da |
| `review-packet/visual-receipt.md` | hash-receipt-artifact | pass | 0e36d9ba168ec4696911104dca6852c07512cbdca15005d3d239819d894658e0 |

## Promotion Blockers

- none

## Safety Boundaries

- local static fixtures and generated artifacts only
- no live market data
- no broker connection
- no order placement
- no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice
- descriptive release-candidate review packet only
