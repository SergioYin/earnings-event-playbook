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

Receipt and handoff outputs are excluded from the receipt inventory so repeated runs remain deterministic and avoid circular handoff hashes.

`export-handoff` reads generated playbook JSON and post-event compare JSON, then writes thesis-ledger and earnings-call-risk-map style Markdown and JSON handoff packs.

```bash
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json --post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json --out demo/handoff.md --json-out demo/handoff.json
```

`--visual-receipt` is optional. When provided, the command carries evidence artifact hashes from the receipt into each handoff pack. The handoff schema includes ticker, fiscal period, source freshness, open review items, thesis note draft, risk map prompts, catalyst follow-up, and evidence artifact hashes. Output is descriptive handoff material and does not recommend any action.

`fixture-gallery` scans one or more local case directories under `examples/cases`. Each case must contain `events.json` and `portfolio.json`; `actuals.json` is optional.

```bash
PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out demo/fixture-gallery.md --json-out demo/fixture-gallery.json
```

The gallery compares cases by tickers, event count, stale source labels, high attention scores, post-event availability, supported demo commands, and safety boundaries.

`tutorial-bundle` writes a deterministic Markdown and JSON reviewer packet for one checked-in case under `examples/cases`.

```bash
PYTHONPATH=src python -m earnings_event_playbook tutorial-bundle --case examples/cases/software --out demo/tutorial-bundle.md --json-out demo/tutorial-bundle.json
```

The tutorial bundle records the tutorial article path, static fixture paths, ordered commands from case playbook through fixture gallery, expected artifact paths, reviewer checklist, maturity rubric evidence, and no-advice safety boundaries. It is a planning and review packet; it does not execute the ordered commands.

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
- Handoff output is deterministic and carries optional receipt hashes for local evidence traceability.
- Fixture gallery output is deterministic and only scans local public case fixture directories.
- Tutorial bundle output is deterministic and only references local public case fixture directories.

## Boundary

All commands operate on local files. The package does not import network clients, read credentials, or call external services.
