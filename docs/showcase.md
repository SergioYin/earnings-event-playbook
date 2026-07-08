# Showcase Landing

`showcase-page` generates `demo/showcase.html` and `demo/showcase.json` as the public first-look surface for this repository.

The HTML file is self-contained and requires no JavaScript, server, API key, network call, broker connection, database, or workflow runner. The JSON file carries the same message in a deterministic manifest for release review and downstream local tooling.

## Generate

```bash
PYTHONPATH=src python -m earnings_event_playbook showcase-page --out demo/showcase.html --json-out demo/showcase.json
```

`demo-bundle --out demo` also writes the showcase artifacts before creating the visual receipt, so receipt hashes include the landing page and manifest.

## Manifest Coverage

`demo/showcase.json` contains:

- Value proposition for local earnings-event review artifacts.
- Quickstart commands for demo bundle, showcase, fixture gallery, tutorial bundle, and selfcheck.
- Demo artifact links for showcase, playbook, post-event compare, visual receipt, handoff, gallery, and tutorial outputs.
- Release evidence for docs, manifest, public hygiene, tests, and package boundary.
- Maturity rubric entries for cold-user clarity, artifact completeness, package hygiene, and safety posture.
- Case gallery highlights for software, retail, and semiconductor fixtures.
- Tutorial path from `docs/tutorial-software-case.md` through deterministic reviewer artifacts.
- Risk boundaries for local static fixtures and descriptive research review only.
- Star-worthy differentiation focused on zero dependencies, paired human and JSON artifacts, no-JavaScript HTML, and a careful public finance-adjacent boundary.

## Safety Boundaries

- Local static fixtures only.
- No live market data.
- No broker connection.
- No order placement.
- No personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice.
- Descriptive research review and release evidence only.

## Review Checklist

- Open `demo/showcase.html` directly in a browser and confirm it renders without JavaScript.
- Compare `demo/showcase.json` against the page sections.
- Confirm links point only at checked-in docs and demo artifacts.
- Run `PYTHONPATH=src python -m earnings_event_playbook selfcheck`.
- Run the test suite before release.
