# Evidence Ledger

`evidence-ledger` builds a deterministic maintainer evidence ledger from existing local release evidence.

```bash
PYTHONPATH=src python -m earnings_event_playbook evidence-ledger \
  --release-manifest release_manifest.json \
  --review-manifest demo/review-packet/review-packet-manifest.json \
  --coldstart-audit demo/coldstart-audit.json \
  --out demo/evidence-ledger.md \
  --json-out demo/evidence-ledger.json
```

## Inputs

- `release_manifest.json`: package version, generated artifact list, verification commands, runtime dependency count, workflow boundary, and safety boundaries.
- `demo/review-packet/review-packet-manifest.json`: ordered review packet commands, artifact roles, media types, byte sizes, SHA-256 hashes, release gate checks, promotion notes, risk boundaries, and next review prompts.
- `demo/coldstart-audit.json`: clone-read-run-trust-promote score, docs checks, exact quickstart commands, artifact hash checks, release gate checks, and promotion blockers.
- Git metadata when available: commit SHA and short commit only. Branch names, local refs, absolute paths, and dirty file lists are not embedded.

## Outputs

- `demo/evidence-ledger.md`: human-readable maintainer evidence ledger.
- `demo/evidence-ledger.json`: machine-readable evidence ledger with sorted JSON keys.

The JSON contains:

- `source_manifests`
- `git_metadata`
- `release_artifacts`
- `review_packet_artifacts`
- `commands`
- `maturity_rubric_mapping`
- `consistency_checks`
- `risk_boundaries`
- `next_evidence_requests`
- `public_hygiene`

## Consistency Checks

The ledger records pass/fail checks for:

- package version alignment across package metadata, release manifest, review packet manifest, and cold-start audit
- review packet artifacts listed in `release_manifest.json`
- cold-start audit coverage of review packet artifacts
- review packet release gates
- cold-start promotion status
- workflow absence

## Boundary

The command reads local files only. It does not fetch data, execute workflows, connect to brokers, place orders, provide personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice, or perform external validation.
