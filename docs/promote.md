# Promotion Checklist

Use this checklist before publishing v1.1.0 release collateral.

## Launch Checks

- Regenerate the review packet: `PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet`.
- Run verification: `PYTHONPATH=src python -m pytest`, `PYTHONPATH=src python -m earnings_event_playbook selfcheck`, and `UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation`.
- Open `demo/review-packet/showcase.html` and capture one desktop screenshot.
- Open `demo/review-packet/playbook.md`, `demo/review-packet/scenario-notebook.md`, and `demo/review-packet/portfolio-drift-bridge.md`; capture one scrolling GIF or short screen recording that shows the packet flow.
- Attach or reference `demo/review-packet/review-packet-manifest.json` as the release evidence manifest.
- Confirm `release_manifest.json`, `CHANGELOG.md`, `pyproject.toml`, `src/earnings_event_playbook/__init__.py`, and `skills/agent/earnings-event-playbook/SKILL.md` all name v1.1.0.

## Risk Copy

This release is a local research artifact generator. It uses static fixtures only, does not fetch live market data, does not connect to brokers, does not place orders, and does not provide personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice.
