# Usage

## Commands

`build-playbook` reads local events and portfolio fixtures and writes Markdown plus JSON.

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
```

`demo-bundle` writes demo fixtures and all demo outputs.

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
```

`selfcheck` scans public package files for private markers and confirms no workflow directory is required.
When run from an installed package, it scans the packaged module boundary instead of the caller's current directory.

```bash
PYTHONPATH=src python -m earnings_event_playbook selfcheck
```

## Output Contract

- Markdown is deterministic and intended for human review.
- JSON is deterministic, sorted, and intended for downstream local tooling.
- HTML is static and does not require JavaScript.

## Boundary

All commands operate on local files. The package does not import network clients, read credentials, or call external services.
