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

Receipt, handoff, scenario notebook, and portfolio drift bridge outputs are excluded from the receipt inventory so repeated runs remain deterministic and avoid circular hashes.

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

`showcase-page` writes a self-contained no-JavaScript landing page plus JSON manifest for the public demo surface.

```bash
PYTHONPATH=src python -m earnings_event_playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json
```

The showcase manifest summarizes value proposition, quickstart commands, demo artifact links, release evidence, maturity rubric, case gallery highlights, tutorial path, risk boundaries, and star-worthy differentiation. It is static release collateral; it does not fetch data or provide advice.

`scenario-notebook` reads generated playbook JSON, handoff JSON, fixture gallery JSON, and optional tutorial/showcase manifests, then writes one Markdown and JSON reviewer notebook.

```bash
PYTHONPATH=src python -m earnings_event_playbook scenario-notebook --playbook demo/playbook.json --handoff demo/handoff.json --fixture-gallery demo/fixture-gallery.json --manifest demo/tutorial-bundle.json demo/showcase.json --out demo/scenario-notebook.md --json-out demo/scenario-notebook.json
```

The notebook covers thesis assumptions, scenario bands, source freshness, evidence hashes, comparison aftermath, next-action queue, fixture gallery summary, optional manifest summary, risk boundary checklist, reusable agent prompts, and safety boundaries. It is a reviewer artifact; it does not fetch data, execute manifests, or provide action recommendations.

`portfolio-drift-bridge` reads a portfolio fixture, scenario notebook JSON, post-event compare JSON, and optional static risk threshold JSON, then writes Markdown and JSON portfolio drift bridge packets.

```bash
PYTHONPATH=src python -m earnings_event_playbook portfolio-drift-bridge --portfolio examples/portfolio.json --scenario-notebook demo/scenario-notebook.json --post-event-compare demo/post-event-compare.json --risk-thresholds examples/risk-thresholds.json --out demo/portfolio-drift-bridge.md --json-out demo/portfolio-drift-bridge.json
```

`--risk-thresholds` is optional. When provided, it must be a local static JSON object with a `thresholds` object such as `examples/risk-thresholds.json`. The output covers exposure concentration, event-linked tickers, scenario mismatch alerts, post-event drift watchlist rows, next risk review prompts, threshold values, and no-trade safety boundaries. It does not fetch data, connect to brokers, place orders, or provide action recommendations.

`review-packet` regenerates the complete release review packet and writes a JSON manifest with command evidence, relative artifact paths, file roles, byte sizes, SHA-256 hashes, release gate checks, promotion notes, and risk boundaries.

```bash
PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet
```

See `docs/review-packet.md` for the manifest contract and reproducibility check. The command uses local static fixtures only and does not fetch data, connect to brokers, place orders, or provide action recommendations.

`coldstart-audit` reads README, docs, demo paths, and a review packet manifest, then writes Markdown plus JSON readiness evidence.

```bash
PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json
```

The audit scores clone, read, run, trust, and promote readiness. It records missing-doc checks, exact README quickstart commands, artifact existence and SHA-256 checks, release gate checks, and promotion blockers. It does not fetch data, execute workflows, connect to brokers, place orders, or provide action recommendations.

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
- Showcase output is deterministic, self-contained, and does not require JavaScript or a server.
- Scenario notebook output is deterministic and combines existing local generated artifacts without executing external workflows.
- Portfolio drift bridge output is deterministic and combines local portfolio, scenario notebook, post-event compare, and optional static threshold artifacts without executing trades or external workflows.
- Review packet output is deterministic and records relative paths plus SHA-256 hashes for local release evidence.
- Cold-start audit output is deterministic and records docs coverage, exact quickstart commands, manifest artifact hash checks, and promotion blockers without external validation.

## Boundary

All commands operate on local files. The package does not import network clients, read credentials, or call external services.
