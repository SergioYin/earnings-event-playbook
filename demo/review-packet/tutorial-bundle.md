# Tutorial Bundle: software

> Deterministic tutorial packet for local static fixtures. Descriptive research review only; no live data, broker connection, orders, or personalized investment, legal, tax, accounting, buy, sell, or hold advice.

## Scope

- Case: `software`
- Case fixtures: `examples/cases/software`
- Output root: `review-packet`
- Tutorial article: `docs/tutorial-software-case.md`

## Static Fixtures

- `examples/cases/software/events.json`
- `examples/cases/software/portfolio.json`
- `examples/cases/software/actuals.json`

## Ordered Commands

### 1. build case playbook

```bash
PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/cases/software/events.json --portfolio examples/cases/software/portfolio.json --out review-packet/cases/software/playbook.md --json-out review-packet/cases/software/playbook.json
```

Expected artifacts:
- `review-packet/cases/software/playbook.md`
- `review-packet/cases/software/playbook.json`

### 2. compare post-event actuals

```bash
PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook review-packet/cases/software/playbook.json --actuals examples/cases/software/actuals.json --out review-packet/cases/software/post-event-compare.md --json-out review-packet/cases/software/post-event-compare.json
```

Expected artifacts:
- `review-packet/cases/software/post-event-compare.md`
- `review-packet/cases/software/post-event-compare.json`

### 3. create visual receipt

```bash
PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts review-packet/cases/software --out review-packet/cases/software/visual-receipt.md --json-out review-packet/cases/software/visual-receipt.json
```

Expected artifacts:
- `review-packet/cases/software/visual-receipt.md`
- `review-packet/cases/software/visual-receipt.json`

### 4. export handoff pack

```bash
PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook review-packet/cases/software/playbook.json --post-event-compare review-packet/cases/software/post-event-compare.json --visual-receipt review-packet/cases/software/visual-receipt.json --out review-packet/cases/software/handoff.md --json-out review-packet/cases/software/handoff.json
```

Expected artifacts:
- `review-packet/cases/software/handoff.md`
- `review-packet/cases/software/handoff.json`

### 5. refresh fixture gallery

```bash
PYTHONPATH=src python -m earnings_event_playbook fixture-gallery --cases examples/cases/software examples/cases/retail examples/cases/semiconductor --out review-packet/fixture-gallery.md --json-out review-packet/fixture-gallery.json
```

Expected artifacts:
- `review-packet/fixture-gallery.md`
- `review-packet/fixture-gallery.json`

## Reviewer Checklist

- [ ] Confirm the static fixture paths are local files under examples/cases.
- [ ] Regenerate the case playbook and compare Markdown against the JSON outputs.
- [ ] Open the visual receipt and confirm expected artifact roles, sizes, and SHA-256 hashes are present.
- [ ] Review the handoff pack for open review items, thesis-note draft language, risk-map prompts, and evidence hashes.
- [ ] Refresh the fixture gallery and confirm the software case is represented with post-event actuals available.
- [ ] Confirm all outputs remain descriptive research review artifacts with no buy, sell, hold, allocation, or order language.

## Maturity Rubric Evidence

### cold-user path

- one tutorial article
- one deterministic tutorial bundle
- ordered commands from fixtures through review artifacts

### artifact traceability

- Markdown and JSON playbook outputs
- post-event comparison outputs
- visual receipt hashes
- handoff evidence references

### public package boundary

- zero runtime dependencies
- local static fixtures only
- no workflow files
- selfcheck private-marker scan

### safety language

- no live market data
- no broker connection
- no order placement
- no personalized investment, legal, tax, accounting, buy, sell, or hold advice

## Safety Boundaries

- local static fixtures only
- no live market data
- no broker connection
- no order placement
- no personalized investment, legal, tax, accounting, buy, sell, or hold advice
- descriptive research review only
