# Cold-Start Audit

`coldstart-audit` scores whether a fresh reviewer can clone, read, run, trust, and promote the package from checked-in public evidence.

```bash
PYTHONPATH=src python -m earnings_event_playbook coldstart-audit --manifest demo/review-packet/review-packet-manifest.json --out demo/coldstart-audit.md --json-out demo/coldstart-audit.json
```

The command reads `README.md`, `docs/usage.md`, `docs/review-packet.md`, `docs/release-readiness.md`, `docs/promote.md`, `docs/coldstart-audit.md`, and `demo/review-packet/review-packet-manifest.json`. It also checks each artifact listed by the manifest against local file existence and SHA-256 hashes.

## Output

- Clone readiness: package version and README quickstart availability.
- Read readiness: required public docs and expected terms.
- Run readiness: exact README quickstart commands and release gate checks.
- Trust readiness: manifest artifact existence and hash matches.
- Promote readiness: blocker-free release state.

The output includes Markdown and JSON forms with missing-doc checks, exact quickstart commands, artifact hash checks, release gates, promotion blockers, and safety boundaries. It is deterministic release-readiness evidence only; it does not fetch data, execute workflows, connect to brokers, place orders, or provide action recommendations.
