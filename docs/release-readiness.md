# Maturity Evidence

Concise evidence for the GitHub asset maturity rubric. This project is positioned as a small public MVP for deterministic earnings-event research artifacts, not as a trading or market-data system.

## Cold-User Readiness

- README first screen states the target user, star reason, zero-dependency promise, quickstart, and fastest demo path.
- Software case tutorial lives at `docs/tutorial-software-case.md`; the deterministic tutorial packet is checked in at `demo/tutorial-bundle.md` and `demo/tutorial-bundle.json`.
- Static demo is checked in at `demo/index.html`; it can be opened directly without JavaScript or a server.
- Human-readable demo output is checked in at `demo/playbook.md`, `demo/post-event-compare.md`, `demo/visual-receipt.md`, and `demo/handoff.md`; deterministic machine output is checked in at `demo/playbook.json`, `demo/post-event-compare.json`, `demo/visual-receipt.json`, and `demo/handoff.json`.
- Multi-case gallery output is checked in at `demo/fixture-gallery.md` and `demo/fixture-gallery.json`.
- Usage docs live in `docs/usage.md`; examples live in `examples/events.json`, `examples/portfolio.json`, `examples/actuals.json`, and `examples/cases`.

## Asset Evidence

- Package source: `src/earnings_event_playbook`
- CLI entry: `python -m earnings_event_playbook`
- Console script: `earnings-event-playbook`
- Fixtures: `examples/events.json`, `examples/portfolio.json`, `examples/actuals.json`
- Case fixtures: `examples/cases/software`, `examples/cases/retail`, `examples/cases/semiconductor`
- Demo outputs: `demo/events.json`, `demo/portfolio.json`, `demo/actuals.json`, `demo/playbook.md`, `demo/playbook.json`, `demo/post-event-compare.md`, `demo/post-event-compare.json`, `demo/index.html`, `demo/visual-receipt.md`, `demo/visual-receipt.json`, `demo/handoff.md`, `demo/handoff.json`
- Gallery outputs: `demo/fixture-gallery.md`, `demo/fixture-gallery.json`, and per-case outputs under `demo/cases`
- Tutorial outputs: `demo/tutorial-bundle.md`, `demo/tutorial-bundle.json`, and `docs/tutorial-software-case.md`
- Agent skill: `skills/agent/earnings-event-playbook/SKILL.md`
- License: `LICENSE`
- Changelog: `CHANGELOG.md`
- Security policy: `SECURITY.md`
- Contribution notes: `CONTRIBUTING.md`

## Verification

```bash
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m unittest discover
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out demo/fixture-gallery.md --json-out demo/fixture-gallery.json
PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json
PYTHONPATH=src python -m earnings_event_playbook selfcheck
uv build
```

Latest local run on 2026-07-08: pytest passed with 26 tests, unittest discovery passed, demo regeneration completed, documented build-playbook completed, documented post-event compare completed, visual receipt regeneration completed, handoff export completed, fixture gallery regeneration completed, tutorial bundle regeneration completed, selfcheck scanned 62 public files, and `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation` produced both 0.6.0 sdist and wheel artifacts.

## Risk Boundaries

- Local static fixtures only.
- No live market data fetching.
- No broker connection.
- No order placement, staging, or recommendation.
- No personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Post-event compare output is descriptive thesis-ledger handoff material, not advice or a recommendation.
- Cross-asset handoff output is descriptive thesis-ledger and earnings-call-risk-map material, not advice or a recommendation.
- Fixture gallery output summarizes local synthetic case coverage only and does not rank or recommend securities.
- Tutorial bundle output is a deterministic review packet for local synthetic case coverage only and does not rank or recommend securities.
- Fixture outputs must be checked against source materials before use.
- Visual receipts record local demo artifact roles, sizes, and SHA-256 hashes; handoff packs can carry those hashes as local evidence references. They are release evidence, not an audit or compliance system.
- GitHub Actions workflows are intentionally not included.

## Current Maturity

- Stage: alpha public MVP.
- Runtime dependencies: 0.
- Public hygiene: selfcheck scans package files for private markers and verifies workflow absence.
- Release shape: source package, CLI, tutorial case study, examples, checked-in demo artifacts, tests, docs, license, changelog, security policy, and contribution notes.
- Known limits: static fixtures are deliberately small; scoring and band matching are heuristic; no external data validation is performed.
