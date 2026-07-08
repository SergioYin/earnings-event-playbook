# Earnings Event Playbook

Use this skill when a user wants to build or review a local earnings event playbook from static fixtures.

## Workflow

1. Confirm the user is working with local JSON fixtures, not live market data or broker accounts.
2. Use `earnings-event-playbook build-playbook --events <events.json> --portfolio <portfolio.json> --out <playbook.md> --json-out <playbook.json>`.
3. Use `earnings-event-playbook compare-post-event --before-playbook <playbook.json> --actuals <actuals.json> --out <compare.md> --json-out <compare.json>` for local post-event comparisons.
4. Use `earnings-event-playbook visual-receipt --artifacts <dir> --out <receipt.md> --json-out <receipt.json>` when local artifact hashes are needed.
5. Use `earnings-event-playbook export-handoff --playbook <playbook.json> --post-event-compare <compare.json> --visual-receipt <receipt.json> --out <handoff.md> --json-out <handoff.json>` for thesis-ledger and earnings-call-risk-map style handoff packs.
6. Use `earnings-event-playbook fixture-gallery --cases <case-dir>... --out <gallery.md> --json-out <gallery.json>` to compare checked-in local case fixtures.
7. Use `earnings-event-playbook tutorial-bundle --case <case-dir> --out <tutorial.md> --json-out <tutorial.json>` when the user needs a deterministic tutorial packet with ordered commands, expected artifact paths, reviewer checklist, maturity rubric evidence, and safety boundaries.
8. Use `earnings-event-playbook showcase-page --out <showcase.html> --json-out <showcase.json>` when the user needs a no-JavaScript landing page and manifest summarizing value proposition, quickstart commands, demo links, release evidence, maturity rubric, case highlights, tutorial path, risk boundaries, and star-worthy differentiation.
9. Use `earnings-event-playbook scenario-notebook --playbook <playbook.json> --handoff <handoff.json> --fixture-gallery <gallery.json> --manifest <manifest.json>... --out <notebook.md> --json-out <notebook.json>` when the user needs one reviewer notebook covering thesis assumptions, scenario bands, source freshness, evidence hashes, comparison aftermath, next-action queue, risk boundary checklist, and reusable agent prompts.
10. Use `earnings-event-playbook portfolio-drift-bridge --portfolio <portfolio.json> --scenario-notebook <notebook.json> --post-event-compare <compare.json> --risk-thresholds <thresholds.json> --out <bridge.md> --json-out <bridge.json>` when the user needs exposure concentration, event-linked tickers, scenario mismatch alerts, post-event drift watchlist rows, next risk review prompts, and no-trade safety boundaries from local artifacts. `--risk-thresholds` is optional and must be static JSON when used.
11. Use `earnings-event-playbook review-packet --out <dir>` when the user needs the v1.2.0 deterministic release packet with copied static inputs, generated Markdown/HTML/JSON artifacts, relative manifest paths, artifact roles, SHA-256 hashes, release gate checks, promotion notes, and risk boundaries.
12. Use `earnings-event-playbook coldstart-audit --manifest <review-packet-manifest.json> --out <audit.md> --json-out <audit.json>` when the user needs clone-read-run-trust-promote readiness scoring with missing-doc checks, exact quickstart commands, artifact existence and hash checks, and promotion blockers.
13. Use `earnings-event-playbook demo-bundle --out <dir>` when the user needs a complete example bundle.
14. Keep all language framed as research review, not advice.

## Boundaries

- No live data fetching.
- No broker connection.
- No order placement.
- No personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Use generic public wording and avoid private environment references.
