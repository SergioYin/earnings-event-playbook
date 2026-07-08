# Maturity Evidence

Concise evidence for the GitHub asset maturity rubric. This project is positioned as a small public MVP for deterministic earnings-event research artifacts, not as a trading or market-data system.

## Cold-User Readiness

- README first screen states the target user, star reason, zero-dependency promise, quickstart, and fastest demo path.
- Static demo is checked in at `demo/index.html`; it can be opened directly without JavaScript or a server.
- Human-readable demo output is checked in at `demo/playbook.md`; deterministic machine output is checked in at `demo/playbook.json`.
- Usage docs live in `docs/usage.md`; examples live in `examples/events.json` and `examples/portfolio.json`.

## Asset Evidence

- Package source: `src/earnings_event_playbook`
- CLI entry: `python -m earnings_event_playbook`
- Console script: `earnings-event-playbook`
- Fixtures: `examples/events.json`, `examples/portfolio.json`
- Demo outputs: `demo/playbook.md`, `demo/playbook.json`, `demo/index.html`
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
PYTHONPATH=src python -m earnings_event_playbook selfcheck
uv build
```

Latest local run on 2026-07-08: pytest passed with 14 tests, unittest discovery passed, demo regeneration completed, selfcheck scanned 31 public files, and `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation` produced both sdist and wheel artifacts.

## Risk Boundaries

- Local static fixtures only.
- No live market data fetching.
- No broker connection.
- No order placement, staging, or recommendation.
- No personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Fixture outputs must be checked against source materials before use.
- GitHub Actions workflows are intentionally not included.

## Current Maturity

- Stage: alpha public MVP.
- Runtime dependencies: 0.
- Public hygiene: selfcheck scans package files for private markers and verifies workflow absence.
- Release shape: source package, CLI, examples, checked-in demo artifacts, tests, docs, license, changelog, security policy, and contribution notes.
- Known limits: static fixtures are deliberately small; scoring is heuristic; no external data validation is performed.
