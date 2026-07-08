# Usage

## Commands

`build-playbook` reads local events and portfolio fixtures and writes Markdown plus JSON.

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json --portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json
```

`compare-post-event` reads a generated playbook JSON file and local actuals fixture, then writes a Markdown and JSON post-event comparison.

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json --actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json
```

The comparison models actual EPS, actual revenue, and actual post-event move outcomes against consensus fields and scenario bands from the before-playbook. It produces thesis-ledger handoff notes and a review status of `ready-for-ledger`, `needs-review`, `needs-data`, or `blocked-missing-actuals`.

`demo-bundle` writes demo fixtures and all demo outputs.

```bash
PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo
```

`visual-receipt` scans local HTML, Markdown, and JSON demo artifacts and writes Markdown plus JSON evidence receipts with file roles, byte sizes, SHA-256 hashes, regeneration commands, review checklist, and safety boundaries.

```bash
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo --out demo/visual-receipt.md --json-out demo/visual-receipt.json
```

Receipt outputs are excluded from their own inventory so repeated runs remain deterministic.

`selfcheck` scans public package files for private markers and confirms no workflow directory is required.
When run from an installed package, it scans the packaged module boundary instead of the caller's current directory.

```bash
PYTHONPATH=src python -m earnings_event_playbook selfcheck
```

## Output Contract

- Markdown is deterministic and intended for human review.
- JSON is deterministic, sorted, and intended for downstream local tooling.
- HTML is static and does not require JavaScript.
- Post-event compare output is descriptive and does not provide action recommendations.
- Visual receipt output is deterministic and records file hashes for local demo review evidence.

## Boundary

All commands operate on local files. The package does not import network clients, read credentials, or call external services.
