# Maturity Evidence

Concise evidence for the GitHub asset maturity rubric. This project is positioned as a small public MVP for deterministic earnings-event research artifacts, not as a trading or market-data system.

## Cold-User Readiness

- README first screen states the target user, star reason, zero-dependency promise, quickstart, and fastest demo path.
- Static demo is checked in at `demo/index.html`; it can be opened directly without JavaScript or a server.
- Human-readable demo output is checked in at `demo/playbook.md` and `demo/post-event-compare.md`; deterministic machine output is checked in at `demo/playbook.json` and `demo/post-event-compare.json`.
- Usage docs live in `docs/usage.md`; examples live in `examples/events.json`, `examples/portfolio.json`, and `examples/actuals.json`.

## Asset Evidence

- Package source: `src/earnings_event_playbook`
- CLI entry: `python -m earnings_event_playbook`
- Console script: `earnings-event-playbook`
- Fixtures: `examples/events.json`, `examples/portfolio.json`, `examples/actuals.json`
- Demo outputs: `demo/events.json`, `demo/portfolio.json`, `demo/actuals.json`, `demo/playbook.md`, `demo/playbook.json`, `demo/post-event-compare.md`, `demo/post-event-compare.json`, `demo/index.html`
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
PYTHONPATH=src python -m earnings_event_playbook selfcheck
uv build
```

Latest local run on 2026-07-08: pytest passed with 18 tests, unittest discovery passed, demo regeneration completed, documented post-event compare completed, selfcheck scanned 35 public files, and `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation` produced both 0.2.0 sdist and wheel artifacts.

## Risk Boundaries

- Local static fixtures only.
- No live market data fetching.
- No broker connection.
- No order placement, staging, or recommendation.
- No personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Post-event compare output is descriptive thesis-ledger handoff material, not advice or a recommendation.
- Fixture outputs must be checked against source materials before use.
- GitHub Actions workflows are intentionally not included.

## Current Maturity

- Stage: alpha public MVP.
- Runtime dependencies: 0.
- Public hygiene: selfcheck scans package files for private markers and verifies workflow absence.
- Release shape: source package, CLI, examples, checked-in demo artifacts, tests, docs, license, changelog, security policy, and contribution notes.
- Known limits: static fixtures are deliberately small; scoring and band matching are heuristic; no external data validation is performed.
