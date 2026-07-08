# Maturity Evidence

Concise evidence for the GitHub asset maturity rubric. This project is positioned as a small public MVP for deterministic earnings-event research artifacts, not as a trading or market-data system.

## Cold-User Readiness

- README first screen states the target user, star reason, zero-dependency promise, quickstart, and fastest demo path.
- Showcase docs live at `docs/showcase.md`; the checked-in showcase landing page and manifest live at `demo/showcase.html` and `demo/showcase.json`.
- Software case tutorial lives at `docs/tutorial-software-case.md`; the deterministic tutorial packet is checked in at `demo/tutorial-bundle.md` and `demo/tutorial-bundle.json`.
- Static demo is checked in at `demo/index.html`; it can be opened directly without JavaScript or a server.
- Human-readable demo output is checked in at `demo/playbook.md`, `demo/post-event-compare.md`, `demo/visual-receipt.md`, and `demo/handoff.md`; deterministic machine output is checked in at `demo/playbook.json`, `demo/post-event-compare.json`, `demo/visual-receipt.json`, and `demo/handoff.json`.
- Multi-case gallery output is checked in at `demo/fixture-gallery.md` and `demo/fixture-gallery.json`.
- Usage docs live in `docs/usage.md`; examples live in `examples/events.json`, `examples/portfolio.json`, `examples/actuals.json`, and `examples/cases`.
- Scenario reviewer notebook output is checked in at `demo/scenario-notebook.md` and `demo/scenario-notebook.json`.
- Portfolio drift bridge output is checked in at `demo/portfolio-drift-bridge.md` and `demo/portfolio-drift-bridge.json`.
- Review packet docs live at `docs/review-packet.md`; the checked-in release packet and manifest live under `demo/review-packet`.
- Promotion checklist lives at `docs/promote.md`.

## Asset Evidence

- Package source: `src/earnings_event_playbook`
- CLI entry: `python -m earnings_event_playbook`
- Console script: `earnings-event-playbook`
- Fixtures: `examples/events.json`, `examples/portfolio.json`, `examples/actuals.json`, `examples/risk-thresholds.json`
- Case fixtures: `examples/cases/software`, `examples/cases/retail`, `examples/cases/semiconductor`
- Demo outputs: `demo/events.json`, `demo/portfolio.json`, `demo/actuals.json`, `demo/playbook.md`, `demo/playbook.json`, `demo/post-event-compare.md`, `demo/post-event-compare.json`, `demo/index.html`, `demo/visual-receipt.md`, `demo/visual-receipt.json`, `demo/handoff.md`, `demo/handoff.json`
- Showcase outputs: `demo/showcase.html`, `demo/showcase.json`, and `docs/showcase.md`
- Gallery outputs: `demo/fixture-gallery.md`, `demo/fixture-gallery.json`, and per-case outputs under `demo/cases`
- Tutorial outputs: `demo/tutorial-bundle.md`, `demo/tutorial-bundle.json`, and `docs/tutorial-software-case.md`
- Scenario notebook outputs: `demo/scenario-notebook.md` and `demo/scenario-notebook.json`
- Portfolio drift bridge outputs: `demo/portfolio-drift-bridge.md` and `demo/portfolio-drift-bridge.json`
- Review packet outputs: `demo/review-packet` and `demo/review-packet/review-packet-manifest.json`
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
PYTHONPATH=src python -m earnings_event_playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json
PYTHONPATH=src python -m earnings_event_playbook scenario-notebook --playbook demo/playbook.json --handoff demo/handoff.json --fixture-gallery demo/fixture-gallery.json --manifest demo/tutorial-bundle.json demo/showcase.json --out demo/scenario-notebook.md --json-out demo/scenario-notebook.json
PYTHONPATH=src python -m earnings_event_playbook portfolio-drift-bridge --portfolio examples/portfolio.json --scenario-notebook demo/scenario-notebook.json --post-event-compare demo/post-event-compare.json --risk-thresholds examples/risk-thresholds.json --out demo/portfolio-drift-bridge.md --json-out demo/portfolio-drift-bridge.json
PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet
PYTHONPATH=src python -m earnings_event_playbook selfcheck
UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation
```

Latest local run on 2026-07-08: pytest passed, demo regeneration completed, documented build-playbook completed, documented post-event compare completed, visual receipt regeneration completed, handoff export completed, fixture gallery regeneration completed, tutorial bundle regeneration completed, showcase page regeneration completed, scenario notebook regeneration completed, portfolio drift bridge regeneration completed, review packet regeneration completed, selfcheck passed, and `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation` produced v1.1.0 sdist and wheel artifacts.

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
- Showcase output is static release collateral for local synthetic artifacts only and does not rank or recommend securities.
- Scenario notebook output combines local generated artifacts into a descriptive reviewer packet only and does not rank or recommend securities.
- Portfolio drift bridge output connects local portfolio exposure, scenario mismatches, post-event drift rows, risk review prompts, and no-trade boundaries; it does not rank or recommend securities.
- Review packet output is deterministic release evidence with relative paths and local artifact hashes only; it does not fetch data, connect to brokers, place orders, or provide action recommendations.
- Fixture outputs must be checked against source materials before use.
- Visual receipts record local demo artifact roles, sizes, and SHA-256 hashes; handoff packs can carry those hashes as local evidence references. They are release evidence, not an audit or compliance system.
- GitHub Actions workflows are intentionally not included.

## Current Maturity

- Stage: alpha public MVP.
- Runtime dependencies: 0.
- Public hygiene: selfcheck scans package files for private markers and verifies workflow absence.
- Release shape: source package, CLI, showcase landing page, scenario notebook, portfolio drift bridge, review packet manifest, tutorial case study, examples, checked-in demo artifacts, tests, docs, license, changelog, security policy, and contribution notes.
- Known limits: static fixtures are deliberately small; scoring and band matching are heuristic; no external data validation is performed.
