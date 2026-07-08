# Earnings Event Playbook

Use this skill when a user wants to build or review a local earnings event playbook from static fixtures.

## Workflow

1. Confirm the user is working with local JSON fixtures, not live market data or broker accounts.
2. Use `earnings-event-playbook build-playbook --events <events.json> --portfolio <portfolio.json> --out <playbook.md> --json-out <playbook.json>`.
3. Use `earnings-event-playbook demo-bundle --out <dir>` when the user needs a complete example bundle.
4. Keep all language framed as research review, not advice.

## Boundaries

- No live data fetching.
- No broker connection.
- No order placement.
- No personalized investment, legal, tax, accounting, buy, sell, or hold advice.
- Use generic public wording and avoid private environment references.
