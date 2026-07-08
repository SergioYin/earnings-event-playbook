from __future__ import annotations

import html
import hashlib
import json
from pathlib import Path
from typing import Iterable, List

from .models import CaseGallery, EventPlaybook, HandoffPack, PostEventComparison


VISUAL_RECEIPT_SAFETY_BOUNDARIES = [
    "local static artifacts only",
    "no live market data",
    "no broker connection",
    "no order placement",
    "no personalized investment advice",
]

VISUAL_RECEIPT_REVIEW_CHECKLIST = [
    "Open demo/index.html directly in a browser and confirm the static preview renders.",
    "Review demo/playbook.md for event fields, scenario bands, risk questions, and review queue items.",
    "Review demo/post-event-compare.md for actuals comparisons, matched scenarios, and ledger handoff notes.",
    "Compare JSON artifacts against Markdown outputs for matching tickers, periods, and review counts.",
    "Confirm receipt hashes after regenerating the demo artifacts.",
]

VISUAL_RECEIPT_REGENERATION_COMMANDS = [
    "PYTHONPATH=src python -m earnings_event_playbook demo-bundle --out demo",
    (
        "PYTHONPATH=src python -m earnings_event_playbook build-playbook --events examples/events.json "
        "--portfolio examples/portfolio.json --out demo/playbook.md --json-out demo/playbook.json"
    ),
    (
        "PYTHONPATH=src python -m earnings_event_playbook compare-post-event --before-playbook demo/playbook.json "
        "--actuals examples/actuals.json --out demo/post-event-compare.md --json-out demo/post-event-compare.json"
    ),
    (
        "PYTHONPATH=src python -m earnings_event_playbook visual-receipt --artifacts demo "
        "--out demo/visual-receipt.md --json-out demo/visual-receipt.json"
    ),
    (
        "PYTHONPATH=src python -m earnings_event_playbook export-handoff --playbook demo/playbook.json "
        "--post-event-compare demo/post-event-compare.json --visual-receipt demo/visual-receipt.json "
        "--out demo/handoff.md --json-out demo/handoff.json"
    ),
]

VISUAL_RECEIPT_SUFFIXES = {".html", ".md", ".json"}

TUTORIAL_REVIEWER_CHECKLIST = [
    "Confirm the static fixture paths are local files under examples/cases.",
    "Regenerate the case playbook and compare Markdown against the JSON outputs.",
    "Open the visual receipt and confirm expected artifact roles, sizes, and SHA-256 hashes are present.",
    "Review the handoff pack for open review items, thesis-note draft language, risk-map prompts, and evidence hashes.",
    "Refresh the fixture gallery and confirm the software case is represented with post-event actuals available.",
    "Confirm all outputs remain descriptive research review artifacts with no buy, sell, hold, allocation, or order language.",
]

TUTORIAL_MATURITY_RUBRIC = [
    {
        "area": "cold-user path",
        "evidence": [
            "one tutorial article",
            "one deterministic tutorial bundle",
            "ordered commands from fixtures through review artifacts",
        ],
    },
    {
        "area": "artifact traceability",
        "evidence": [
            "Markdown and JSON playbook outputs",
            "post-event comparison outputs",
            "visual receipt hashes",
            "handoff evidence references",
        ],
    },
    {
        "area": "public package boundary",
        "evidence": [
            "zero runtime dependencies",
            "local static fixtures only",
            "no workflow files",
            "selfcheck private-marker scan",
        ],
    },
    {
        "area": "safety language",
        "evidence": [
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment, legal, tax, accounting, buy, sell, or hold advice",
        ],
    },
]

TUTORIAL_SAFETY_BOUNDARIES = [
    "local static fixtures only",
    "no live market data",
    "no broker connection",
    "no order placement",
    "no personalized investment, legal, tax, accounting, buy, sell, or hold advice",
    "descriptive research review only",
]


def playbooks_to_dict(playbooks: Iterable[EventPlaybook]) -> dict:
    items = [item.to_dict() for item in playbooks]
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "safety_boundaries": [
            "local static fixtures only",
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment advice",
        ],
        "playbooks": items,
    }


def render_json(playbooks: Iterable[EventPlaybook]) -> str:
    return json.dumps(playbooks_to_dict(playbooks), indent=2, sort_keys=True) + "\n"


def render_fixture_gallery_json(gallery: CaseGallery) -> str:
    return json.dumps(gallery.to_dict(), indent=2, sort_keys=True) + "\n"


def render_fixture_gallery_markdown(gallery: CaseGallery) -> str:
    data = gallery.to_dict()
    summary = data["summary"]
    lines: List[str] = [
        "# Fixture Case Gallery",
        "",
        "> Educational fixture comparison only. Local static fixtures only; no live data, broker connection, orders, or investment advice.",
        "",
        "## Summary",
        "",
        f"- Cases: {summary['case_count']}",
        f"- Events: {summary['event_count']}",
        f"- Tickers: {', '.join(summary['tickers']) if summary['tickers'] else 'None'}",
        f"- Stale source flags: {summary['stale_source_count']}",
        f"- High attention flags: {summary['high_attention_count']}",
        f"- Cases with post-event actuals: {summary['post_event_case_count']}",
        "",
        "## Case Comparison",
        "",
        "| Case | Tickers | Events | Stale sources | High attention | Post-event availability |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    for case in data["cases"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{case['case_id']}`",
                    ", ".join(case["tickers"]) or "None",
                    str(case["event_count"]),
                    _gallery_list(case["stale_sources"]),
                    _gallery_attention(case["high_attention_scores"]),
                    _gallery_post_event(case),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Supported Demo Commands", ""])
    for case in data["cases"]:
        lines.extend([f"### {case['case_id']}", ""])
        for command in case["supported_demo_commands"]:
            lines.extend(["```bash", command, "```", ""])
    lines.extend(["## Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in data["safety_boundaries"])
    return "\n".join(lines).rstrip() + "\n"


def build_tutorial_bundle(case_id: str, case_path: str, output_root: str, has_actuals: bool) -> dict:
    case_output_root = f"{output_root}/cases/{case_id}"
    static_fixtures = [
        f"{case_path}/events.json",
        f"{case_path}/portfolio.json",
    ]
    if has_actuals:
        static_fixtures.append(f"{case_path}/actuals.json")
    commands = [
        {
            "step": 1,
            "name": "build case playbook",
            "command": (
                "PYTHONPATH=src python -m earnings_event_playbook build-playbook "
                f"--events {case_path}/events.json --portfolio {case_path}/portfolio.json "
                f"--out {case_output_root}/playbook.md --json-out {case_output_root}/playbook.json"
            ),
            "expected_artifacts": [
                f"{case_output_root}/playbook.md",
                f"{case_output_root}/playbook.json",
            ],
        },
        {
            "step": 2,
            "name": "compare post-event actuals",
            "command": (
                "PYTHONPATH=src python -m earnings_event_playbook compare-post-event "
                f"--before-playbook {case_output_root}/playbook.json --actuals {case_path}/actuals.json "
                f"--out {case_output_root}/post-event-compare.md "
                f"--json-out {case_output_root}/post-event-compare.json"
            ),
            "expected_artifacts": [
                f"{case_output_root}/post-event-compare.md",
                f"{case_output_root}/post-event-compare.json",
            ],
            "requires_actuals_fixture": True,
        },
        {
            "step": 3,
            "name": "create visual receipt",
            "command": (
                "PYTHONPATH=src python -m earnings_event_playbook visual-receipt "
                f"--artifacts {case_output_root} --out {case_output_root}/visual-receipt.md "
                f"--json-out {case_output_root}/visual-receipt.json"
            ),
            "expected_artifacts": [
                f"{case_output_root}/visual-receipt.md",
                f"{case_output_root}/visual-receipt.json",
            ],
        },
        {
            "step": 4,
            "name": "export handoff pack",
            "command": (
                "PYTHONPATH=src python -m earnings_event_playbook export-handoff "
                f"--playbook {case_output_root}/playbook.json "
                f"--post-event-compare {case_output_root}/post-event-compare.json "
                f"--visual-receipt {case_output_root}/visual-receipt.json "
                f"--out {case_output_root}/handoff.md --json-out {case_output_root}/handoff.json"
            ),
            "expected_artifacts": [
                f"{case_output_root}/handoff.md",
                f"{case_output_root}/handoff.json",
            ],
        },
        {
            "step": 5,
            "name": "refresh fixture gallery",
            "command": (
                "PYTHONPATH=src python -m earnings_event_playbook fixture-gallery "
                "--cases examples/cases/software examples/cases/retail examples/cases/semiconductor "
                f"--out {output_root}/fixture-gallery.md --json-out {output_root}/fixture-gallery.json"
            ),
            "expected_artifacts": [
                f"{output_root}/fixture-gallery.md",
                f"{output_root}/fixture-gallery.json",
            ],
        },
    ]
    if not has_actuals:
        commands[1]["status"] = "skipped-until-actuals-fixture-exists"
        commands[3]["status"] = "skipped-until-post-event-compare-exists"
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "tutorial-bundle",
        "case_id": case_id,
        "case_path": case_path,
        "output_root": output_root,
        "tutorial_article": "docs/tutorial-software-case.md",
        "static_fixtures": static_fixtures,
        "ordered_commands": commands,
        "reviewer_checklist": TUTORIAL_REVIEWER_CHECKLIST,
        "maturity_rubric_evidence": TUTORIAL_MATURITY_RUBRIC,
        "safety_boundaries": TUTORIAL_SAFETY_BOUNDARIES,
    }


def render_tutorial_bundle_json(bundle: dict) -> str:
    return json.dumps(bundle, indent=2, sort_keys=True) + "\n"


def render_tutorial_bundle_markdown(bundle: dict) -> str:
    lines: List[str] = [
        f"# Tutorial Bundle: {bundle['case_id']}",
        "",
        "> Deterministic tutorial packet for local static fixtures. Descriptive research review only; no live data, broker connection, orders, or personalized investment, legal, tax, accounting, buy, sell, or hold advice.",
        "",
        "## Scope",
        "",
        f"- Case: `{bundle['case_id']}`",
        f"- Case fixtures: `{bundle['case_path']}`",
        f"- Output root: `{bundle['output_root']}`",
        f"- Tutorial article: `{bundle['tutorial_article']}`",
        "",
        "## Static Fixtures",
        "",
    ]
    lines.extend(f"- `{path}`" for path in bundle["static_fixtures"])
    lines.extend(["", "## Ordered Commands", ""])
    for command in bundle["ordered_commands"]:
        lines.extend(
            [
                f"### {command['step']}. {command['name']}",
                "",
                "```bash",
                command["command"],
                "```",
                "",
                "Expected artifacts:",
            ]
        )
        lines.extend(f"- `{path}`" for path in command["expected_artifacts"])
        if "status" in command:
            lines.append(f"- Status: `{command['status']}`")
        lines.append("")
    lines.extend(["## Reviewer Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in bundle["reviewer_checklist"])
    lines.extend(["", "## Maturity Rubric Evidence", ""])
    for item in bundle["maturity_rubric_evidence"]:
        lines.append(f"### {item['area']}")
        lines.append("")
        lines.extend(f"- {evidence}" for evidence in item["evidence"])
        lines.append("")
    lines.extend(["## Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in bundle["safety_boundaries"])
    return "\n".join(lines).rstrip() + "\n"


def post_event_to_dict(comparisons: Iterable[PostEventComparison]) -> dict:
    items = [item.to_dict() for item in comparisons]
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "post-event-compare",
        "safety_boundaries": [
            "local static fixtures only",
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment advice",
        ],
        "comparisons": items,
    }


def render_post_event_json(comparisons: Iterable[PostEventComparison]) -> str:
    return json.dumps(post_event_to_dict(comparisons), indent=2, sort_keys=True) + "\n"


def handoff_to_dict(packs: Iterable[HandoffPack]) -> dict:
    items = [item.to_dict() for item in packs]
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "cross-asset-handoff",
        "workflows": ["thesis-ledger", "earnings-call-risk-map"],
        "safety_boundaries": [
            "local static artifacts only",
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment advice",
        ],
        "handoff_packs": items,
    }


def render_handoff_json(packs: Iterable[HandoffPack]) -> str:
    return json.dumps(handoff_to_dict(packs), indent=2, sort_keys=True) + "\n"


def build_visual_receipt(artifact_root: Path, project_root: Path | None = None) -> dict:
    root = artifact_root.resolve()
    if not root.exists():
        raise ValueError(f"{artifact_root} does not exist")
    if not root.is_dir():
        raise ValueError(f"{artifact_root} must be a directory")

    base = project_root.resolve() if project_root is not None else root.parent
    files = [_visual_receipt_file(path, base) for path in sorted(root.rglob("*")) if _is_visual_artifact(path)]
    role_counts: dict[str, int] = {}
    for file_item in files:
        role_counts[file_item["role"]] = role_counts.get(file_item["role"], 0) + 1

    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "visual-receipt",
        "artifact_root": _relative_path(root, base),
        "summary": {
            "file_count": len(files),
            "total_bytes": sum(file_item["size_bytes"] for file_item in files),
            "roles": dict(sorted(role_counts.items())),
        },
        "files": files,
        "regeneration_commands": VISUAL_RECEIPT_REGENERATION_COMMANDS,
        "review_checklist": VISUAL_RECEIPT_REVIEW_CHECKLIST,
        "safety_boundaries": VISUAL_RECEIPT_SAFETY_BOUNDARIES,
    }


def render_visual_receipt_json(receipt: dict) -> str:
    return json.dumps(receipt, indent=2, sort_keys=True) + "\n"


def render_visual_receipt_markdown(receipt: dict) -> str:
    summary = receipt["summary"]
    lines: List[str] = [
        "# Visual Evidence Receipt",
        "",
        "> Deterministic receipt for local demo artifacts. Static files only; no live data, broker connection, orders, or recommendations.",
        "",
        "## Summary",
        "",
        f"- Artifact root: `{receipt['artifact_root']}`",
        f"- Files scanned: {summary['file_count']}",
        f"- Total bytes: {summary['total_bytes']}",
        "",
        "## File Roles",
        "",
    ]
    for role, count in summary["roles"].items():
        lines.append(f"- {role}: {count}")
    if not summary["roles"]:
        lines.append("- None")
    lines.extend(
        [
            "",
            "## Artifact Inventory",
            "",
            "| Path | Role | Bytes | SHA-256 |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for file_item in receipt["files"]:
        lines.append(
            f"| `{file_item['path']}` | {file_item['role']} | {file_item['size_bytes']} | "
            f"`{file_item['sha256']}` |"
        )
    lines.extend(["", "## Regeneration Commands", ""])
    for command in receipt["regeneration_commands"]:
        lines.extend(["```bash", command, "```", ""])
    lines.extend(["## Review Checklist", ""])
    lines.extend(f"- [ ] {item}" for item in receipt["review_checklist"])
    lines.extend(["", "## Safety Boundaries", ""])
    lines.extend(f"- {item}" for item in receipt["safety_boundaries"])
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(playbooks: Iterable[EventPlaybook]) -> str:
    items = list(playbooks)
    lines: List[str] = [
        "# Earnings Event Playbook",
        "",
        "> Educational research review only. Local static fixtures only; no live data, broker connection, orders, or investment advice.",
        "",
        "## Summary",
        "",
        f"- Events: {len(items)}",
        f"- Review queue items: {sum(len(item.review_queue) for item in items)}",
        "",
    ]
    for item in items:
        event = item.event
        lines.extend(
            [
                f"## {event.ticker} - {event.company}",
                "",
                f"- Event date: {event.date.isoformat()}",
                f"- Fiscal period: {event.fiscal_period}",
                f"- Consensus EPS: {_fmt_number(event.consensus_eps)}",
                f"- Consensus revenue: {_fmt_number(event.consensus_revenue)}",
                f"- Implied move: {event.implied_move_percent:.2f}%",
                f"- Source: {event.source_name} ({event.source_date.isoformat()}, {item.freshness})",
                f"- Attention score: {item.attention_score}/100",
                "",
                "### Position",
                "",
            ]
        )
        if item.position is None:
            lines.append("- No matching portfolio position in fixture.")
        else:
            position = item.position
            lines.extend(
                [
                    f"- Shares: {position.shares:g}",
                    f"- Exposure: {position.exposure:.2f}",
                    f"- Portfolio weight: {position.portfolio_weight_percent:.2f}%",
                    f"- Notes: {position.notes or 'None'}",
                ]
            )
        lines.extend(["", "### Scenario Bands", "", "| Scenario | Price move | EPS delta | Revenue delta | Exposure delta |", "| --- | ---: | ---: | ---: | ---: |"])
        for band in item.scenario_bands:
            lines.append(
                f"| {band.name} | {band.price_move_percent:.2f}% | {band.eps_delta_percent:.2f}% | "
                f"{band.revenue_delta_percent:.2f}% | {band.exposure_delta:.2f} |"
            )
        lines.extend(["", "### Thesis Sensitivities", ""])
        if item.thesis_sensitivities:
            for sensitivity in item.thesis_sensitivities:
                lines.append(f"- **{sensitivity.topic}** ({sensitivity.risk_weight}): {sensitivity.note}")
        else:
            lines.append("- None provided.")
        lines.extend(["", "### Risk Questions", ""])
        if item.risk_questions:
            lines.extend(f"- {question}" for question in item.risk_questions)
        else:
            lines.append("- None provided.")
        lines.extend(["", "### Post-Event Review Queue", ""])
        lines.extend(f"- {entry}" for entry in item.review_queue)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _is_visual_artifact(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() in VISUAL_RECEIPT_SUFFIXES
        and not path.name.startswith("visual-receipt.")
        and not path.name.startswith("handoff.")
    )


def _visual_receipt_file(path: Path, base: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": _relative_path(path.resolve(), base),
        "role": _visual_receipt_role(path),
        "media_type": _visual_receipt_media_type(path),
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _visual_receipt_role(path: Path) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name == "index.html":
        return "static-html-preview"
    if suffix == ".html":
        return "html-artifact"
    if suffix == ".md" and "post-event" in name:
        return "post-event-markdown"
    if suffix == ".json" and "post-event" in name:
        return "post-event-json"
    if suffix == ".md" and "playbook" in name:
        return "playbook-markdown"
    if suffix == ".json" and "playbook" in name:
        return "playbook-json"
    if suffix == ".md" and "handoff" in name:
        return "handoff-markdown"
    if suffix == ".json" and "handoff" in name:
        return "handoff-json"
    if suffix == ".json" and name in {"events.json", "portfolio.json", "actuals.json"}:
        return "input-fixture"
    if suffix == ".md":
        return "markdown-artifact"
    return "json-artifact"


def _visual_receipt_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".html":
        return "text/html"
    if suffix == ".md":
        return "text/markdown"
    return "application/json"


def _relative_path(path: Path, base: Path) -> str:
    try:
        return path.relative_to(base).as_posix()
    except ValueError:
        return path.name


def render_post_event_markdown(comparisons: Iterable[PostEventComparison]) -> str:
    items = list(comparisons)
    lines: List[str] = [
        "# Post-Event Compare",
        "",
        "> Educational research review only. Local static fixtures only; no live data, broker connection, orders, or investment advice.",
        "",
        "## Summary",
        "",
        f"- Comparisons: {len(items)}",
        f"- Review queue items: {sum(len(item.review_queue) for item in items)}",
        "",
    ]
    for item in items:
        event = item.event
        lines.extend(
            [
                f"## {event.ticker} - {event.company}",
                "",
                f"- Fiscal period: {event.fiscal_period}",
                f"- Event date: {event.date.isoformat()}",
                f"- Review status: {item.review_status}",
            ]
        )
        if item.actual is None:
            lines.append("- Actuals source: not matched")
        else:
            actual = item.actual
            lines.extend(
                [
                    f"- Report date: {actual.report_date.isoformat()}",
                    f"- Actuals source: {actual.source_name} ({actual.source_date.isoformat()})",
                    f"- Actuals note: {actual.notes or 'None'}",
                ]
            )
        lines.extend(
            [
                "",
                "### Outcome Comparison",
                "",
                "| Metric | Consensus | Actual | Delta | Delta % | Band |",
                "| --- | ---: | ---: | ---: | ---: | --- |",
                _metric_row("EPS", item.eps),
                _metric_row("Revenue", item.revenue),
                "",
                "### Move Comparison",
                "",
                "| Implied move | Actual move | Delta | Matched scenario |",
                "| ---: | ---: | ---: | --- |",
                (
                    f"| {item.move.implied_move_percent:.2f}% | {_fmt_percent(item.move.actual_move_percent)} | "
                    f"{_fmt_percent(item.move.delta_percent)} | {item.move.matched_scenario} |"
                ),
                "",
                "### Thesis Ledger Handoff",
                "",
            ]
        )
        lines.extend(f"- {note}" for note in item.thesis_ledger_handoff)
        lines.extend(["", "### Review Queue", ""])
        lines.extend(f"- {entry}" for entry in item.review_queue)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_handoff_markdown(packs: Iterable[HandoffPack]) -> str:
    items = list(packs)
    lines: List[str] = [
        "# Cross-Asset Handoff Pack",
        "",
        "> Educational research handoff only. Local static artifacts only; no live data, broker connection, orders, or investment advice.",
        "",
        "## Summary",
        "",
        f"- Handoff packs: {len(items)}",
        f"- Open review items: {sum(len(item.open_review_items) for item in items)}",
        f"- Evidence hashes attached: {sum(len(item.evidence_artifact_hashes) for item in items)}",
        "",
        "## Workflows",
        "",
        "- thesis-ledger",
        "- earnings-call-risk-map",
        "",
    ]
    for item in items:
        lines.extend(
            [
                f"## {item.ticker} - {item.company}",
                "",
                f"- Fiscal period: {item.fiscal_period}",
                f"- Source freshness: {item.source_freshness}",
                f"- Event source: {item.event_source_name} ({item.event_source_date.isoformat()})",
                f"- Actuals source: {item.actual_source_name} ({_fmt_date_or_none(item.actual_source_date)})",
                f"- Review status: {item.review_status}",
                "",
                "### Thesis Note Draft",
                "",
                item.thesis_note_draft,
                "",
                "### Open Review Items",
                "",
            ]
        )
        lines.extend(f"- {entry}" for entry in item.open_review_items)
        lines.extend(["", "### Risk Map Prompts", ""])
        lines.extend(f"- {prompt}" for prompt in item.risk_map_prompts)
        lines.extend(["", "### Catalyst Follow-Up", ""])
        lines.extend(f"- {entry}" for entry in item.catalyst_follow_up)
        lines.extend(["", "### Evidence Artifact Hashes", ""])
        if item.evidence_artifact_hashes:
            lines.extend(["| Path | Role | Bytes | SHA-256 |", "| --- | --- | ---: | --- |"])
            for artifact in item.evidence_artifact_hashes:
                lines.append(
                    f"| `{artifact.path}` | {artifact.role} | {artifact.size_bytes} | `{artifact.sha256}` |"
                )
        else:
            lines.append("- None provided.")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html_index(playbooks: Iterable[EventPlaybook]) -> str:
    items = list(playbooks)
    cards = []
    for item in items:
        event = item.event
        review_items = "".join(f"<li>{html.escape(entry)}</li>" for entry in item.review_queue)
        risk_questions = "".join(f"<li>{html.escape(question)}</li>" for question in item.risk_questions)
        if not risk_questions:
            risk_questions = "<li>None provided.</li>"
        cards.append(
            "<section class=\"card\">"
            f"<h2>{html.escape(event.ticker)} - {html.escape(event.company)}</h2>"
            f"<p><strong>Event:</strong> {event.date.isoformat()} | "
            f"<strong>Period:</strong> {html.escape(event.fiscal_period)} | "
            f"<strong>Freshness:</strong> {html.escape(item.freshness)}</p>"
            f"<p><strong>Attention:</strong> {item.attention_score}/100 | "
            f"<strong>Implied move:</strong> {event.implied_move_percent:.2f}%</p>"
            "<table><thead><tr><th>Scenario</th><th>Price move</th><th>Exposure delta</th></tr></thead><tbody>"
            + "".join(
                f"<tr><td>{html.escape(band.name)}</td><td>{band.price_move_percent:.2f}%</td><td>{band.exposure_delta:.2f}</td></tr>"
                for band in item.scenario_bands
            )
            + "</tbody></table>"
            "<div class=\"grid\">"
            "<div><h3>Risk questions</h3><ul>" + risk_questions + "</ul></div>"
            "<div><h3>Review queue</h3><ul>" + review_items + "</ul></div>"
            "</div>"
            "</section>"
        )
    total_review_items = sum(len(item.review_queue) for item in items)
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Earnings Event Playbook Demo</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; color: #1f2933; background: #f7f8fa; }
    header { background: #12343b; color: white; padding: 32px max(24px, 8vw); }
    main { max-width: 1040px; margin: 0 auto; padding: 24px; }
    .notice { border-left: 4px solid #d9822b; background: #fff8f0; padding: 12px 16px; }
    .card { background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 18px; margin: 18px 0; }
    .summary { display: flex; flex-wrap: wrap; gap: 12px; margin: 18px 0; }
    .summary div { background: white; border: 1px solid #d9e2ec; padding: 12px 14px; min-width: 150px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 16px; }
    table { border-collapse: collapse; width: 100%; margin-top: 12px; }
    th, td { border-bottom: 1px solid #e4e7eb; padding: 8px; text-align: left; }
    th { background: #f0f4f8; }
    h3 { margin-bottom: 8px; }
    ul { margin-top: 0; padding-left: 20px; }
  </style>
</head>
<body>
  <header>
    <h1>Earnings Event Playbook Demo</h1>
    <p>Static local-fixture preview. No JavaScript, live data, broker connection, orders, or advice.</p>
  </header>
  <main>
    <p class="notice">Use this page as a review artifact only. Verify any fixture data against source materials before making decisions.</p>
    <section class="summary" aria-label="Demo summary">
      <div><strong>Events</strong><br>""" + str(len(items)) + """</div>
      <div><strong>Review items</strong><br>""" + str(total_review_items) + """</div>
      <div><strong>Runtime deps</strong><br>0</div>
      <div><strong>Data mode</strong><br>local fixtures</div>
    </section>
    """ + "\n    ".join(cards) + """
  </main>
</body>
</html>
"""


def _fmt_number(value: float | None) -> str:
    if value is None:
        return "not provided"
    return f"{value:.2f}"


def _fmt_percent(value: float | None) -> str:
    if value is None:
        return "not provided"
    return f"{value:.2f}%"


def _fmt_date_or_none(value) -> str:
    if value is None:
        return "not provided"
    return value.isoformat()


def _gallery_list(items: List[str]) -> str:
    return ", ".join(items) if items else "None"


def _gallery_attention(items: List[dict]) -> str:
    if not items:
        return "None"
    return ", ".join(f"{item['ticker']} {item['score']}" for item in items)


def _gallery_post_event(case: dict) -> str:
    if not case["post_event_available"]:
        return "No actuals fixture"
    return f"{case['post_event_match_count']}/{case['event_count']} matched"


def _metric_row(label: str, comparison) -> str:
    return (
        f"| {label} | {_fmt_number(comparison.consensus)} | {_fmt_number(comparison.actual)} | "
        f"{_fmt_number(comparison.delta)} | {_fmt_percent(comparison.delta_percent)} | {comparison.band} |"
    )
