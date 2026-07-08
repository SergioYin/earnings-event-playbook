# Review Packet

`review-packet` generates the release review bundle in one deterministic pass. It copies the public local fixtures into the packet, regenerates the core Markdown, HTML, and JSON artifacts, then writes `review-packet-manifest.json` with command evidence, file roles, byte sizes, and SHA-256 hashes.

```bash
PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet
```

The checked-in packet lives under `demo/review-packet`. The manifest is the entry point for reviewers who need to verify what was generated and whether the release gates passed.

## Contents

- `inputs/events.json`, `inputs/portfolio.json`, `inputs/actuals.json`, and `inputs/risk-thresholds.json`: copied static input fixtures.
- `playbook.md` and `playbook.json`: pre-event scenario review output.
- `post-event-compare.md` and `post-event-compare.json`: actuals comparison output.
- `fixture-gallery.md` and `fixture-gallery.json`: multi-case fixture coverage.
- `tutorial-bundle.md` and `tutorial-bundle.json`: software case tutorial packet.
- `showcase.html` and `showcase.json`: static no-JavaScript showcase page and manifest.
- `visual-receipt.md` and `visual-receipt.json`: hash receipt for packet artifacts available at receipt time.
- `handoff.md` and `handoff.json`: cross-asset handoff packs with receipt hash references.
- `scenario-notebook.md` and `scenario-notebook.json`: combined reviewer notebook.
- `portfolio-drift-bridge.md` and `portfolio-drift-bridge.json`: portfolio drift review packet.
- `review-packet-manifest.json`: release evidence manifest.

## Manifest Contract

The manifest uses `schema_version` `1.0` and includes:

- `package_version`: package version used to generate the packet.
- `output_root`: packet-relative root, expected to be `review-packet` for the checked-in demo packet.
- `commands`: ordered command log with completed status and expected artifact paths.
- `artifact_paths`: sorted relative paths for all tracked packet files except the manifest itself.
- `artifacts`: path, role, media type, size, and SHA-256 for each tracked packet file.
- `release_gate_checks`: pass/fail evidence for orchestration, expected artifacts, hash inventory, zero runtime dependencies, workflow boundary, and local static inputs.
- `promotion_gate_notes`, `risk_boundaries`, and `next_review_prompts`: release review copy.

All manifest paths are relative. The packet must not contain absolute local paths, private environment references, workflow files, network instructions, broker instructions, or recommendation language.

## Reproducibility Check

Run the packet generator into a fresh directory with the same basename and compare manifests.

```bash
rm -rf /tmp/eep-a /tmp/eep-b
PYTHONPATH=src python -m earnings_event_playbook review-packet --out /tmp/eep-a/review-packet
PYTHONPATH=src python -m earnings_event_playbook review-packet --out /tmp/eep-b/review-packet
diff -u /tmp/eep-a/review-packet/review-packet-manifest.json /tmp/eep-b/review-packet/review-packet-manifest.json
```

The diff should be empty. For the checked-in release packet, regenerate `demo/review-packet` before tagging and confirm the manifest hash inventory remains stable.

## Release Verification

```bash
PYTHONPATH=src python -m pytest
PYTHONPATH=src python -m earnings_event_playbook selfcheck
PYTHONPATH=src python -m earnings_event_playbook review-packet --out demo/review-packet
UV_CACHE_DIR=/tmp/uv-cache uv build --no-build-isolation
```

The packet is descriptive release evidence only. It uses local static fixtures, does not fetch market data, does not connect to brokers, does not place orders, and does not provide personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice.
