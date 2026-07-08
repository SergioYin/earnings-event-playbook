# Promotion Checklist

Use this checklist before publishing v1.3.0 release collateral.

## Launch Checks

- Regenerate the review packet: `PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet`.
- Regenerate the cold-start audit: `PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json`.
- Regenerate the evidence ledger: `PYTHONPATH=src python -m earnings_event_playbook evidence-ledger --release-manifest release_manifest.json --review-manifest demo/review-packet/review-packet-manifest.json --coldstart-audit demo/coldstart-audit.json --out demo/evidence-ledger.md --json-out demo/evidence-ledger.json`.
- Run verification: `PYTHONPATH=src python -m pytest`, `PYTHONPATH=src python -m earnings_event_playbook selfcheck`, `PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet`, `PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json`, `PYTHONPATH=src python -m earnings_event_playbook evidence-ledger --release-manifest release_manifest.json --review-manifest demo/review-packet/review-packet-manifest.json --coldstart-audit demo/coldstart-audit.json --out demo/evidence-ledger.md --json-out demo/evidence-ledger.json`, and `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation`.
- Open `demo/review-packet/showcase.html` and capture one desktop screenshot.
- Open `demo/review-packet/playbook.md`, `demo/review-packet/scenario-notebook.md`, and `demo/review-packet/portfolio-drift-bridge.md`; capture one scrolling GIF or short screen recording that shows the packet flow.
- Attach or reference `demo/review-packet/review-packet-manifest.json` as the release evidence manifest.
- Attach or reference `demo/coldstart-audit.json` as the clone-read-run-trust-promote readiness evidence.
- Attach or reference `demo/evidence-ledger.json` as the maintainer evidence ledger.
- Confirm `release_manifest.json`, `CHANGELOG.md`, `pyproject.toml`, `src/earnings_event_playbook/__init__.py`, and `skills/agent/earnings-event-playbook/SKILL.md` all name v1.3.0.

## Risk Copy

This release is a local research artifact generator. It uses static fixtures only, does not fetch live market data, does not connect to brokers, does not place orders, and does not provide personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice.
