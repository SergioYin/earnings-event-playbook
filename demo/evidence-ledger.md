# Maintainer Evidence Ledger

- Package version: `1.3.0`
- Release manifest: `release_manifest.json`
- Review packet manifest: `demo/review-packet/review-packet-manifest.json`
- Cold-start audit: `demo/coldstart-audit.json`
- Git metadata: available
- Release artifacts: 59
- Review packet hashed artifacts: 22

## Consistency Checks

| Check | Status | Evidence |
| --- | --- | --- |
| package-version-alignment | pass | release=1.3.0; review=1.3.0; audit=1.3.0; package=1.3.0 |
| review-packet-artifacts-covered-by-release-manifest | pass | 22/22 review packet artifacts listed in release_manifest.json |
| coldstart-audit-covered-review-artifacts | pass | 22/22 review packet artifacts checked by coldstart audit |
| release-gates-pass | pass | 6/6 review packet release gates pass |
| coldstart-promotion-pass | pass | score=100/100; blockers=0 |
| workflow-boundary | pass | workflow_files=none |

## Commands

| Source | Step | Command | Result |
| --- | ---: | --- | --- |
| release_manifest | 1 | `PYTHONPATH=src python -m pytest` | 36 passed |
| release_manifest | 2 | `PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet` | passed |
| release_manifest | 3 | `PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json` | score 100/100, status pass, promotion blockers none |
| release_manifest | 4 | `PYTHONPATH=src python -m earnings_event_playbook evidence-ledger --release-manifest release_manifest.json --review-manifest demo/review-packet/review-packet-manifest.json --coldstart-audit demo/coldstart-audit.json --out demo/evidence-ledger.md --json-out demo/evidence-ledger.json` | passed, 6/6 consistency checks pass |
| release_manifest | 5 | `PYTHONPATH=src python -m earnings_event_playbook selfcheck` | selfcheck ok: version=1.3.0 |
| release_manifest | 6 | `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation` | built dist/earnings_event_playbook-1.3.0.tar.gz and dist/earnings_event_playbook-1.3.0-py3-none-any.whl |
| review_packet_manifest | 1 | `PYTHONPATH=src python -m earnings_event_playbook build-playbook --events review-packet/inputs/events.json --portfolio review-packet/inputs/portfolio.json --out review-packet/playbook.md --json-out review-packet/playbook.json` | completed |
| review_packet_manifest | 2 | `PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook review-packet/playbook.json --actuals review-packet/inputs/actuals.json --out review-packet/post-event-compare.md --json-out review-packet/post-event-compare.json` | completed |
| review_packet_manifest | 3 | `PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out review-packet/fixture-gallery.md --json-out review-packet/fixture-gallery.json` | completed |
| review_packet_manifest | 4 | `PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle --case examples/cases/software --out review-packet/tutorial-bundle.md --json-out review-packet/tutorial-bundle.json` | completed |
| review_packet_manifest | 5 | `PYTHONPATH=src python -m earnings_event_playbook showcase-page --out review-packet/showcase.html --json-out review-packet/showcase.json` | completed |
| review_packet_manifest | 6 | `PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts review-packet --out review-packet/visual-receipt.md --json-out review-packet/visual-receipt.json` | completed |
| review_packet_manifest | 7 | `PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook review-packet/playbook.json --post-event-compare review-packet/post-event-compare.json --visual-receipt review-packet/visual-receipt.json --out review-packet/handoff.md --json-out review-packet/handoff.json` | completed |
| review_packet_manifest | 8 | `PYTHONPATH=src python -m earnings_event_playbook scenario-notebook --playbook review-packet/playbook.json --handoff review-packet/handoff.json --fixture-gallery review-packet/fixture-gallery.json --manifest review-packet/tutorial-bundle.json review-packet/showcase.json --out review-packet/scenario-notebook.md --json-out review-packet/scenario-notebook.json` | completed |
| review_packet_manifest | 9 | `PYTHONPATH=src python -m earnings_event_playbook portfolio-drift-bridge --portfolio review-packet/inputs/portfolio.json --scenario-notebook review-packet/scenario-notebook.json --post-event-compare review-packet/post-event-compare.json --risk-thresholds review-packet/inputs/risk-thresholds.json --out review-packet/portfolio-drift-bridge.md --json-out review-packet/portfolio-drift-bridge.json` | completed |

## Maturity Rubric Mapping

| Area | Status | Evidence |
| --- | --- | --- |
| artifact traceability | pass | 59 release artifacts listed; 22 review packet artifacts hashed; SHA-256 inventory carried from review-packet-manifest.json |
| command reproducibility | pass | 6 release verification commands recorded; 9 review packet generation commands recorded |
| cold-start readiness | pass | score 100/100; 0 promotion blockers |
| package hygiene | pass | runtime_dependencies=0; workflow_files=none |
| risk boundary clarity | pass | local static fixtures only; no live data; no broker connection; no orders; no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice; local static fixtures and generated artifacts only; no live market data; no order placement; descriptive release-candidate review packet only |

## Release Artifact Paths

- `demo/actuals.json`
- `demo/cases/retail/playbook.json`
- `demo/cases/retail/playbook.md`
- `demo/cases/semiconductor/playbook.json`
- `demo/cases/semiconductor/playbook.md`
- `demo/cases/semiconductor/post-event-compare.json`
- `demo/cases/semiconductor/post-event-compare.md`
- `demo/cases/software/playbook.json`
- `demo/cases/software/playbook.md`
- `demo/cases/software/post-event-compare.json`
- `demo/cases/software/post-event-compare.md`
- `demo/coldstart-audit.json`
- `demo/coldstart-audit.md`
- `demo/events.json`
- `demo/evidence-ledger.json`
- `demo/evidence-ledger.md`
- `demo/fixture-gallery.json`
- `demo/fixture-gallery.md`
- `demo/handoff.json`
- `demo/handoff.md`
- `demo/index.html`
- `demo/playbook.json`
- `demo/playbook.md`
- `demo/portfolio-drift-bridge.json`
- `demo/portfolio-drift-bridge.md`
- `demo/portfolio.json`
- `demo/post-event-compare.json`
- `demo/post-event-compare.md`
- `demo/review-packet/fixture-gallery.json`
- `demo/review-packet/fixture-gallery.md`
- `demo/review-packet/handoff.json`
- `demo/review-packet/handoff.md`
- `demo/review-packet/inputs/actuals.json`
- `demo/review-packet/inputs/events.json`
- `demo/review-packet/inputs/portfolio.json`
- `demo/review-packet/inputs/risk-thresholds.json`
- `demo/review-packet/playbook.json`
- `demo/review-packet/playbook.md`
- `demo/review-packet/portfolio-drift-bridge.json`
- `demo/review-packet/portfolio-drift-bridge.md`
- `demo/review-packet/post-event-compare.json`
- `demo/review-packet/post-event-compare.md`
- `demo/review-packet/review-packet-manifest.json`
- `demo/review-packet/scenario-notebook.json`
- `demo/review-packet/scenario-notebook.md`
- `demo/review-packet/showcase.html`
- `demo/review-packet/showcase.json`
- `demo/review-packet/tutorial-bundle.json`
- `demo/review-packet/tutorial-bundle.md`
- `demo/review-packet/visual-receipt.json`
- `demo/review-packet/visual-receipt.md`
- `demo/scenario-notebook.json`
- `demo/scenario-notebook.md`
- `demo/showcase.html`
- `demo/showcase.json`
- `demo/tutorial-bundle.json`
- `demo/tutorial-bundle.md`
- `demo/visual-receipt.json`
- `demo/visual-receipt.md`

## Review Packet Hash Inventory

| Path | Role | SHA-256 |
| --- | --- | --- |
| `review-packet/fixture-gallery.json` | case-gallery-artifact | `3965bf845ee22791be53507c37fe709cebc83111960b10b6614144a1a6c8c35d` |
| `review-packet/fixture-gallery.md` | case-gallery-artifact | `85245a266cacca9861b74e9b9fa097f0982c97bcfebbf140b0fa55326d81f607` |
| `review-packet/handoff.json` | cross-asset-handoff-artifact | `c33ea4601a0a4f99a023ebc3e0acb71b72105fc66449b0b92b14007ba25ea943` |
| `review-packet/handoff.md` | cross-asset-handoff-artifact | `ae6d279706623d71f315debcb1ef9c123212a10c39769e4f637674920cfe0fcb` |
| `review-packet/inputs/actuals.json` | input-fixture | `d6008a8d2888aaf3d9efab7d9b84d5179cf4298428156ecb0a9d46f5a9a59e79` |
| `review-packet/inputs/events.json` | input-fixture | `972654c17ac4816435cbf28207f69822a5acff8db7ef352d7677b3ccb93827cc` |
| `review-packet/inputs/portfolio.json` | input-fixture | `552f2e7c3fec4cd7bc32b642eec760706200adb3d567225dcb15fa981f299e00` |
| `review-packet/inputs/risk-thresholds.json` | input-fixture | `eb05108dbc8bde62cfe54b9a3e4688711ab1c5eb60c7e8b320695aecd9a8bc42` |
| `review-packet/playbook.json` | pre-event-playbook-artifact | `3c94be26c733282f91ddf58012aa8fe93aedd8fe077fff7b7c9bc665169d2b34` |
| `review-packet/playbook.md` | pre-event-playbook-artifact | `59d9451b5206bfa979f0ee224214b1aed2501485246ec230805c982c29354a47` |
| `review-packet/portfolio-drift-bridge.json` | portfolio-drift-artifact | `bc3fa072331df1af64c68360473e114b9891f244f928c00425b3cd7bde3a7f4f` |
| `review-packet/portfolio-drift-bridge.md` | portfolio-drift-artifact | `10436cd2b6083ef9df49df701139956996e7d35b0db3982646ec174b4a3478d0` |
| `review-packet/post-event-compare.json` | post-event-comparison-artifact | `72265335193bb1660508c0d39467c47b718fe85abb0a197da773f4067f26bf79` |
| `review-packet/post-event-compare.md` | post-event-comparison-artifact | `a512dad6c3e4b30322103162bdf56041de775aa52e1a82072edf0b04c95fd1eb` |
| `review-packet/scenario-notebook.json` | scenario-review-artifact | `c54299867c4139c3b8cde479c8e7a7fb9b3495f5af9db6f5c41bc17f30aa16c2` |
| `review-packet/scenario-notebook.md` | scenario-review-artifact | `334c90b2ad744543596931838d58c86ea241490d18f715aa7f7a6eb2ca9ade33` |
| `review-packet/showcase.html` | showcase-artifact | `8ae30d2072c9eda4af70b2d21d3d4c9ca895076d68d55500fb409cd0da60a9ca` |
| `review-packet/showcase.json` | showcase-artifact | `e45ee457692a55de5eaf0a5c3e3ac9f89ac623a3287dbcd62bbf986a2d6d659a` |
| `review-packet/tutorial-bundle.json` | tutorial-artifact | `43fe3db28198add8399d23a5898b5393cb9510ec1209a81a177b53b8655a8c47` |
| `review-packet/tutorial-bundle.md` | tutorial-artifact | `d22f4698d14eaffe4e69dc148466c2d1d5d47166c282beeca50a101e734e30a1` |
| `review-packet/visual-receipt.json` | hash-receipt-artifact | `66bb64e5364745eda38e902833faad8a7b1fc894711bdb85940e7dfc3433a1da` |
| `review-packet/visual-receipt.md` | hash-receipt-artifact | `0e36d9ba168ec4696911104dca6852c07512cbdca15005d3d239819d894658e0` |

## Risk Boundaries

- local static fixtures only
- no live data
- no broker connection
- no orders
- no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice
- local static fixtures and generated artifacts only
- no live market data
- no order placement
- descriptive release-candidate review packet only

## Next Evidence Requests

- Attach regenerated demo/evidence-ledger.md and demo/evidence-ledger.json before tagging.
- Confirm release_manifest.json verification command results match the final local run.
- Confirm review-packet-manifest.json and coldstart-audit.json were regenerated from the same checked-in artifacts.
- Confirm public files contain no private refs, workflow files, credentials, or action language.
- Capture any optional screenshot or package-index evidence outside the repository if needed by the maintainer.

## Public Hygiene

- Absolute paths present: `False`
- Private markers present: `False`
- Workflow files: `none`
