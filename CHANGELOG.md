# Changelog

## 1.1.0

- Added review packet release docs and promotion checklist for deterministic packet review, screenshots/GIF capture, manifest evidence, and risk copy.
- Hardened `review-packet` manifest coverage with explicit artifact roles, relative path checks, SHA-256 determinism tests, and private-reference hygiene assertions.
- Updated README quickstart, usage docs, release evidence, release manifest, agent skill, package version metadata, checked-in review packet artifacts, and tests.

## 0.9.0

- Added `portfolio-drift-bridge` CLI command for bridging portfolio fixture exposure, scenario notebook JSON, post-event compare JSON, and optional static risk thresholds into Markdown and JSON drift packets.
- Added checked-in `examples/risk-thresholds.json`, `demo/portfolio-drift-bridge.md`, and `demo/portfolio-drift-bridge.json` covering exposure concentration, event-linked tickers, scenario mismatch alerts, post-event drift watchlist, next risk review prompts, and no-trade safety boundaries.
- Updated README, usage docs, showcase docs, release evidence, release manifest, agent skill, demo bundle generation, version metadata, and tests.

## 0.8.0

- Added `scenario-notebook` CLI command for combining playbook JSON, handoff JSON, fixture gallery JSON, and optional tutorial/showcase manifests into Markdown and JSON reviewer notebooks.
- Added checked-in `demo/scenario-notebook.md` and `demo/scenario-notebook.json` covering thesis assumptions, scenario bands, source freshness, evidence hashes, comparison aftermath, next-action queue, risk boundary checklist, and reusable agent prompts.
- Updated README, usage docs, showcase docs, release evidence, release manifest, agent skill, demo bundle generation, version metadata, and tests.

## 0.7.0

- Added `showcase-page` CLI command for a self-contained no-JavaScript showcase landing page plus JSON manifest.
- Added `docs/showcase.md`, checked-in `demo/showcase.html`, and checked-in `demo/showcase.json` covering value proposition, quickstart commands, demo links, release evidence, maturity rubric, case highlights, tutorial path, risk boundaries, and star-worthy differentiation.
- Updated README first screen, usage docs, release evidence, release manifest, agent skill, demo bundle generation, version metadata, and CLI tests.

## 0.6.0

- Added `tutorial-bundle` CLI command for deterministic case-study reviewer packets with ordered commands, expected artifact paths, reviewer checklist, maturity rubric evidence, and no-advice safety boundaries.
- Added `docs/tutorial-software-case.md` walkthrough from static software fixtures to playbook, post-event compare, visual receipt, handoff, fixture gallery, and tutorial packet.
- Added checked-in `demo/tutorial-bundle.md` and `demo/tutorial-bundle.json`, README first-screen tutorial CTA, docs, release evidence, manifest updates, agent skill updates, and CLI tests.

## 0.5.0

- Added `fixture-gallery` CLI command for comparing multiple local case fixture directories under `examples/cases`.
- Added gallery Markdown and JSON output covering tickers, event counts, stale sources, high attention scores, post-event availability, supported demo commands, and safety boundaries.
- Added synthetic software, retail, and semiconductor case folders with checked-in per-case demo playbooks, optional post-event comparisons, docs, release evidence, manifest updates, and tests.

## 0.4.0

- Added `export-handoff` CLI command for cross-asset Markdown and JSON handoff packs.
- Added handoff schema fields for ticker, fiscal period, source freshness, open review items, thesis note draft, risk map prompts, catalyst follow-up, and optional visual receipt evidence artifact hashes.
- Added checked-in `demo/handoff.md` and `demo/handoff.json`, docs, release evidence, manifest updates, and parser/render/CLI tests.

## 0.3.0

- Added `visual-receipt` CLI command for local demo artifact evidence receipts.
- Added deterministic Markdown and JSON receipt renderers with file roles, sizes, SHA-256 hashes, regeneration commands, review checklist, and safety boundaries.
- Added checked-in `demo/visual-receipt.md` and `demo/visual-receipt.json`, docs, release evidence, manifest updates, and CLI tests.

## 0.2.0

- Added `compare-post-event` CLI command for local post-event actuals comparison.
- Added actual EPS, revenue, and move outcome modeling against consensus and scenario bands.
- Added thesis-ledger handoff notes, review status, review queue output, demo actuals fixture, demo compare artifacts, docs, and tests.

## 0.1.0

- Initial public-ready MVP.
- Added zero-dependency package, CLI, fixtures, Markdown/JSON/static HTML renderers, tests, docs, agent skill, and MIT license.
