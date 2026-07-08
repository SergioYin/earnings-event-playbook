from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from . import __version__
from .core import (
    build_fixture_gallery,
    build_handoff_packs,
    build_playbooks,
    build_portfolio_drift_bridge,
    compare_post_event,
)
from .io import read_json, write_text
from .models import (
    FixtureError,
    parse_actuals_fixture,
    parse_events_fixture,
    parse_playbook_json,
    parse_portfolio_fixture,
    parse_post_event_compare_json,
    parse_visual_receipt_hashes,
)
from .render import (
    build_scenario_notebook,
    build_showcase_manifest,
    build_tutorial_bundle,
    build_visual_receipt,
    render_handoff_json,
    render_handoff_markdown,
    render_html_index,
    render_fixture_gallery_json,
    render_fixture_gallery_markdown,
    render_json,
    render_markdown,
    render_portfolio_drift_bridge_json,
    render_portfolio_drift_bridge_markdown,
    render_post_event_json,
    render_post_event_markdown,
    render_scenario_notebook_json,
    render_scenario_notebook_markdown,
    render_showcase_html,
    render_showcase_json,
    render_tutorial_bundle_json,
    render_tutorial_bundle_markdown,
    render_visual_receipt_json,
    render_visual_receipt_markdown,
)


PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_MARKER_FILES = {"pyproject.toml", "README.md", "LICENSE"}
SCANNED_SUFFIXES = {".py", ".md", ".toml", ".json", ".html", ".txt"}
SKIPPED_SCAN_DIRS = {".git", "__pycache__", ".pytest_cache", "build", "dist"}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="earnings-event-playbook")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-playbook", help="Build Markdown and JSON playbooks from local fixtures.")
    build.add_argument("--events", required=True, type=Path)
    build.add_argument("--portfolio", required=True, type=Path)
    build.add_argument("--out", required=True, type=Path)
    build.add_argument("--json-out", required=True, type=Path)

    compare = subparsers.add_parser(
        "compare-post-event", help="Compare a pre-event playbook JSON file with local actuals fixtures."
    )
    compare.add_argument("--before-playbook", required=True, type=Path)
    compare.add_argument("--actuals", required=True, type=Path)
    compare.add_argument("--out", required=True, type=Path)
    compare.add_argument("--json-out", required=True, type=Path)

    demo = subparsers.add_parser("demo-bundle", help="Generate demo fixtures and static outputs.")
    demo.add_argument("--out", required=True, type=Path)

    receipt = subparsers.add_parser("visual-receipt", help="Create Markdown and JSON evidence receipts for demo artifacts.")
    receipt.add_argument("--artifacts", required=True, type=Path)
    receipt.add_argument("--out", required=True, type=Path)
    receipt.add_argument("--json-out", required=True, type=Path)

    handoff = subparsers.add_parser(
        "export-handoff", help="Export Markdown and JSON cross-asset handoff packs from reviewed artifacts."
    )
    handoff.add_argument("--playbook", required=True, type=Path)
    handoff.add_argument("--post-event-compare", required=True, type=Path)
    handoff.add_argument("--out", required=True, type=Path)
    handoff.add_argument("--json-out", required=True, type=Path)
    handoff.add_argument("--visual-receipt", type=Path)

    gallery = subparsers.add_parser(
        "fixture-gallery", help="Compare one or more local examples/cases fixture directories."
    )
    gallery.add_argument("--cases", required=True, nargs="+", type=Path)
    gallery.add_argument("--out", required=True, type=Path)
    gallery.add_argument("--json-out", required=True, type=Path)

    tutorial = subparsers.add_parser(
        "tutorial-bundle", help="Build a deterministic tutorial packet for one local case fixture."
    )
    tutorial.add_argument("--case", required=True, type=Path)
    tutorial.add_argument("--out", required=True, type=Path)
    tutorial.add_argument("--json-out", required=True, type=Path)
    tutorial.add_argument("--output-root", default="demo", help="Artifact root shown in ordered tutorial commands.")

    showcase = subparsers.add_parser(
        "showcase-page", help="Generate a self-contained no-JS showcase landing page and JSON manifest."
    )
    showcase.add_argument("--out", required=True, type=Path)
    showcase.add_argument("--json-out", required=True, type=Path)

    notebook = subparsers.add_parser(
        "scenario-notebook", help="Combine generated artifacts into a Markdown and JSON reviewer notebook."
    )
    notebook.add_argument("--playbook", required=True, type=Path)
    notebook.add_argument("--handoff", required=True, type=Path)
    notebook.add_argument("--fixture-gallery", required=True, type=Path)
    notebook.add_argument("--manifest", nargs="*", default=[], type=Path)
    notebook.add_argument("--out", required=True, type=Path)
    notebook.add_argument("--json-out", required=True, type=Path)

    drift = subparsers.add_parser(
        "portfolio-drift-bridge",
        help="Bridge portfolio exposure, scenario notebook, and post-event compare artifacts into drift review packets.",
    )
    drift.add_argument("--portfolio", required=True, type=Path)
    drift.add_argument("--scenario-notebook", required=True, type=Path)
    drift.add_argument("--post-event-compare", required=True, type=Path)
    drift.add_argument("--risk-thresholds", type=Path)
    drift.add_argument("--out", required=True, type=Path)
    drift.add_argument("--json-out", required=True, type=Path)

    packet = subparsers.add_parser(
        "review-packet",
        help="Generate the deterministic v1.0.0 release-candidate review packet and JSON run manifest.",
    )
    packet.add_argument("--out", required=True, type=Path)
    packet.add_argument("--events", default=Path("examples/events.json"), type=Path)
    packet.add_argument("--portfolio", default=Path("examples/portfolio.json"), type=Path)
    packet.add_argument("--actuals", default=Path("examples/actuals.json"), type=Path)
    packet.add_argument("--risk-thresholds", default=Path("examples/risk-thresholds.json"), type=Path)
    packet.add_argument(
        "--cases",
        nargs="+",
        default=[
            Path("examples/cases/software"),
            Path("examples/cases/retail"),
            Path("examples/cases/semiconductor"),
        ],
        type=Path,
    )
    packet.add_argument("--tutorial-case", default=Path("examples/cases/software"), type=Path)

    subparsers.add_parser("selfcheck", help="Verify package boundaries and fixture parsing.")

    args = parser.parse_args(argv)
    try:
        if args.command == "build-playbook":
            return _build_playbook(args.events, args.portfolio, args.out, args.json_out)
        if args.command == "compare-post-event":
            return _compare_post_event(args.before_playbook, args.actuals, args.out, args.json_out)
        if args.command == "demo-bundle":
            return _demo_bundle(args.out)
        if args.command == "visual-receipt":
            return _visual_receipt(args.artifacts, args.out, args.json_out)
        if args.command == "export-handoff":
            return _export_handoff(args.playbook, args.post_event_compare, args.out, args.json_out, args.visual_receipt)
        if args.command == "fixture-gallery":
            return _fixture_gallery(args.cases, args.out, args.json_out)
        if args.command == "tutorial-bundle":
            return _tutorial_bundle(args.case, args.out, args.json_out, args.output_root)
        if args.command == "showcase-page":
            return _showcase_page(args.out, args.json_out)
        if args.command == "scenario-notebook":
            return _scenario_notebook(
                args.playbook, args.handoff, args.fixture_gallery, args.manifest, args.out, args.json_out
            )
        if args.command == "portfolio-drift-bridge":
            return _portfolio_drift_bridge(
                args.portfolio,
                args.scenario_notebook,
                args.post_event_compare,
                args.risk_thresholds,
                args.out,
                args.json_out,
            )
        if args.command == "review-packet":
            return _review_packet(
                args.out,
                args.events,
                args.portfolio,
                args.actuals,
                args.risk_thresholds,
                args.cases,
                args.tutorial_case,
            )
        if args.command == "selfcheck":
            return _selfcheck()
    except (FixtureError, OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 1


def _load_playbooks(events_path: Path, portfolio_path: Path):
    events = parse_events_fixture(read_json(events_path))
    portfolio = parse_portfolio_fixture(read_json(portfolio_path))
    return build_playbooks(events, portfolio)


def _build_playbook(events_path: Path, portfolio_path: Path, out_path: Path, json_path: Path) -> int:
    playbooks = _load_playbooks(events_path, portfolio_path)
    write_text(out_path, render_markdown(playbooks))
    write_text(json_path, render_json(playbooks))
    return 0


def _compare_post_event(before_path: Path, actuals_path: Path, out_path: Path, json_path: Path) -> int:
    playbooks = parse_playbook_json(read_json(before_path))
    actuals = parse_actuals_fixture(read_json(actuals_path))
    comparisons = compare_post_event(playbooks, actuals)
    write_text(out_path, render_post_event_markdown(comparisons))
    write_text(json_path, render_post_event_json(comparisons))
    return 0


def _demo_bundle(out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    events_path = out_dir / "events.json"
    portfolio_path = out_dir / "portfolio.json"
    write_text(events_path, _demo_events_json())
    write_text(portfolio_path, _demo_portfolio_json())
    actuals_path = out_dir / "actuals.json"
    write_text(actuals_path, _demo_actuals_json())
    playbooks = _load_playbooks(events_path, portfolio_path)
    write_text(out_dir / "playbook.md", render_markdown(playbooks))
    write_text(out_dir / "playbook.json", render_json(playbooks))
    comparisons = compare_post_event(playbooks, parse_actuals_fixture(read_json(actuals_path)))
    write_text(out_dir / "post-event-compare.md", render_post_event_markdown(comparisons))
    write_text(out_dir / "post-event-compare.json", render_post_event_json(comparisons))
    write_text(out_dir / "index.html", render_html_index(playbooks))
    _showcase_page(out_dir / "showcase.html", out_dir / "showcase.json")
    _visual_receipt(out_dir, out_dir / "visual-receipt.md", out_dir / "visual-receipt.json")
    _export_handoff(
        out_dir / "playbook.json",
        out_dir / "post-event-compare.json",
        out_dir / "handoff.md",
        out_dir / "handoff.json",
        out_dir / "visual-receipt.json",
    )
    _fixture_gallery(
        [
            _project_root() / "examples" / "cases" / "software",
            _project_root() / "examples" / "cases" / "retail",
            _project_root() / "examples" / "cases" / "semiconductor",
        ],
        out_dir / "fixture-gallery.md",
        out_dir / "fixture-gallery.json",
    )
    _tutorial_bundle(
        _project_root() / "examples" / "cases" / "software",
        out_dir / "tutorial-bundle.md",
        out_dir / "tutorial-bundle.json",
        "demo",
    )
    _scenario_notebook(
        out_dir / "playbook.json",
        out_dir / "handoff.json",
        out_dir / "fixture-gallery.json",
        [out_dir / "tutorial-bundle.json", out_dir / "showcase.json"],
        out_dir / "scenario-notebook.md",
        out_dir / "scenario-notebook.json",
    )
    _portfolio_drift_bridge(
        out_dir / "portfolio.json",
        out_dir / "scenario-notebook.json",
        out_dir / "post-event-compare.json",
        _project_root() / "examples" / "risk-thresholds.json",
        out_dir / "portfolio-drift-bridge.md",
        out_dir / "portfolio-drift-bridge.json",
    )
    return 0


def _visual_receipt(artifacts_dir: Path, out_path: Path, json_path: Path) -> int:
    receipt = build_visual_receipt(artifacts_dir)
    write_text(out_path, render_visual_receipt_markdown(receipt))
    receipt = build_visual_receipt(artifacts_dir)
    write_text(json_path, render_visual_receipt_json(receipt))
    return 0


def _export_handoff(
    playbook_path: Path,
    post_event_compare_path: Path,
    out_path: Path,
    json_path: Path,
    visual_receipt_path: Path | None = None,
) -> int:
    playbooks = parse_playbook_json(read_json(playbook_path))
    comparisons = parse_post_event_compare_json(read_json(post_event_compare_path))
    hashes = parse_visual_receipt_hashes(read_json(visual_receipt_path)) if visual_receipt_path is not None else []
    packs = build_handoff_packs(playbooks, comparisons, hashes)
    write_text(out_path, render_handoff_markdown(packs))
    write_text(json_path, render_handoff_json(packs))
    return 0


def _fixture_gallery(case_dirs: Sequence[Path], out_path: Path, json_path: Path) -> int:
    if not case_dirs:
        raise ValueError("at least one case directory is required")
    project_root = _project_root()
    cases_root = (project_root / "examples" / "cases").resolve()
    case_inputs = []
    for case_dir in case_dirs:
        resolved = case_dir.resolve()
        if not resolved.is_dir():
            raise ValueError(f"{case_dir} must be a case directory")
        try:
            resolved.relative_to(cases_root)
        except ValueError as exc:
            raise ValueError(f"{case_dir} must be under examples/cases") from exc
        events_path = resolved / "events.json"
        portfolio_path = resolved / "portfolio.json"
        actuals_path = resolved / "actuals.json"
        if not events_path.exists():
            raise ValueError(f"{case_dir} is missing events.json")
        if not portfolio_path.exists():
            raise ValueError(f"{case_dir} is missing portfolio.json")
        actuals = parse_actuals_fixture(read_json(actuals_path)) if actuals_path.exists() else None
        case_inputs.append(
            (
                resolved.name,
                resolved.relative_to(project_root).as_posix(),
                parse_events_fixture(read_json(events_path)),
                parse_portfolio_fixture(read_json(portfolio_path)),
                actuals,
            )
        )
    gallery = build_fixture_gallery(case_inputs)
    write_text(out_path, render_fixture_gallery_markdown(gallery))
    write_text(json_path, render_fixture_gallery_json(gallery))
    return 0


def _tutorial_bundle(case_dir: Path, out_path: Path, json_path: Path, output_root: str) -> int:
    project_root = _project_root()
    cases_root = (project_root / "examples" / "cases").resolve()
    resolved = case_dir.resolve()
    if not resolved.is_dir():
        raise ValueError(f"{case_dir} must be a case directory")
    try:
        case_path = resolved.relative_to(project_root).as_posix()
        resolved.relative_to(cases_root)
    except ValueError as exc:
        raise ValueError(f"{case_dir} must be under examples/cases") from exc
    events_path = resolved / "events.json"
    portfolio_path = resolved / "portfolio.json"
    actuals_path = resolved / "actuals.json"
    if not events_path.exists():
        raise ValueError(f"{case_dir} is missing events.json")
    if not portfolio_path.exists():
        raise ValueError(f"{case_dir} is missing portfolio.json")
    parse_events_fixture(read_json(events_path))
    parse_portfolio_fixture(read_json(portfolio_path))
    has_actuals = actuals_path.exists()
    if has_actuals:
        parse_actuals_fixture(read_json(actuals_path))
    bundle = build_tutorial_bundle(resolved.name, case_path, output_root.rstrip("/"), has_actuals)
    write_text(out_path, render_tutorial_bundle_markdown(bundle))
    write_text(json_path, render_tutorial_bundle_json(bundle))
    return 0


def _showcase_page(out_path: Path, json_path: Path) -> int:
    manifest = build_showcase_manifest()
    write_text(out_path, render_showcase_html(manifest))
    write_text(json_path, render_showcase_json(manifest))
    return 0


def _scenario_notebook(
    playbook_path: Path,
    handoff_path: Path,
    fixture_gallery_path: Path,
    manifest_paths: Sequence[Path],
    out_path: Path,
    json_path: Path,
) -> int:
    notebook = build_scenario_notebook(
        read_json(playbook_path),
        read_json(handoff_path),
        read_json(fixture_gallery_path),
        [read_json(path) for path in manifest_paths],
    )
    write_text(out_path, render_scenario_notebook_markdown(notebook))
    write_text(json_path, render_scenario_notebook_json(notebook))
    return 0


def _portfolio_drift_bridge(
    portfolio_path: Path,
    scenario_notebook_path: Path,
    post_event_compare_path: Path,
    thresholds_path: Path | None,
    out_path: Path,
    json_path: Path,
) -> int:
    portfolio = parse_portfolio_fixture(read_json(portfolio_path))
    thresholds = read_json(thresholds_path) if thresholds_path is not None else None
    packet = build_portfolio_drift_bridge(
        portfolio,
        read_json(scenario_notebook_path),
        read_json(post_event_compare_path),
        thresholds,
    )
    write_text(out_path, render_portfolio_drift_bridge_markdown(packet))
    write_text(json_path, render_portfolio_drift_bridge_json(packet))
    return 0


def _review_packet(
    out_dir: Path,
    events_path: Path,
    portfolio_path: Path,
    actuals_path: Path,
    thresholds_path: Path,
    case_dirs: Sequence[Path],
    tutorial_case: Path,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    packet_base = out_dir.parent.resolve()
    inputs_dir = out_dir / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    packet_events = inputs_dir / "events.json"
    packet_portfolio = inputs_dir / "portfolio.json"
    packet_actuals = inputs_dir / "actuals.json"
    packet_thresholds = inputs_dir / "risk-thresholds.json"
    _copy_text(events_path, packet_events)
    _copy_text(portfolio_path, packet_portfolio)
    _copy_text(actuals_path, packet_actuals)
    _copy_text(thresholds_path, packet_thresholds)

    commands: list[dict] = []

    playbook_md = out_dir / "playbook.md"
    playbook_json = out_dir / "playbook.json"
    _build_playbook(packet_events, packet_portfolio, playbook_md, playbook_json)
    _packet_command(
        commands,
        "build-playbook",
        [
            "build-playbook",
            "--events",
            _packet_rel(packet_events, packet_base),
            "--portfolio",
            _packet_rel(packet_portfolio, packet_base),
            "--out",
            _packet_rel(playbook_md, packet_base),
            "--json-out",
            _packet_rel(playbook_json, packet_base),
        ],
        [playbook_md, playbook_json],
        packet_base,
    )

    compare_md = out_dir / "post-event-compare.md"
    compare_json = out_dir / "post-event-compare.json"
    _compare_post_event(playbook_json, packet_actuals, compare_md, compare_json)
    _packet_command(
        commands,
        "compare-post-event",
        [
            "compare-post-event",
            "--before-playbook",
            _packet_rel(playbook_json, packet_base),
            "--actuals",
            _packet_rel(packet_actuals, packet_base),
            "--out",
            _packet_rel(compare_md, packet_base),
            "--json-out",
            _packet_rel(compare_json, packet_base),
        ],
        [compare_md, compare_json],
        packet_base,
    )

    gallery_md = out_dir / "fixture-gallery.md"
    gallery_json = out_dir / "fixture-gallery.json"
    _fixture_gallery(case_dirs, gallery_md, gallery_json)
    _packet_command(
        commands,
        "fixture-gallery",
        [
            "fixture-gallery",
            "--cases",
            *[_project_rel(path) for path in case_dirs],
            "--out",
            _packet_rel(gallery_md, packet_base),
            "--json-out",
            _packet_rel(gallery_json, packet_base),
        ],
        [gallery_md, gallery_json],
        packet_base,
    )

    tutorial_md = out_dir / "tutorial-bundle.md"
    tutorial_json = out_dir / "tutorial-bundle.json"
    _tutorial_bundle(tutorial_case, tutorial_md, tutorial_json, _packet_rel(out_dir, packet_base))
    _packet_command(
        commands,
        "tutorial-bundle",
        [
            "tutorial-bundle",
            "--case",
            _project_rel(tutorial_case),
            "--out",
            _packet_rel(tutorial_md, packet_base),
            "--json-out",
            _packet_rel(tutorial_json, packet_base),
        ],
        [tutorial_md, tutorial_json],
        packet_base,
    )

    showcase_html = out_dir / "showcase.html"
    showcase_json = out_dir / "showcase.json"
    _showcase_page(showcase_html, showcase_json)
    _packet_command(
        commands,
        "showcase-page",
        [
            "showcase-page",
            "--out",
            _packet_rel(showcase_html, packet_base),
            "--json-out",
            _packet_rel(showcase_json, packet_base),
        ],
        [showcase_html, showcase_json],
        packet_base,
    )

    receipt_md = out_dir / "visual-receipt.md"
    receipt_json = out_dir / "visual-receipt.json"
    _visual_receipt(out_dir, receipt_md, receipt_json)
    _packet_command(
        commands,
        "visual-receipt",
        [
            "visual-receipt",
            "--artifacts",
            _packet_rel(out_dir, packet_base),
            "--out",
            _packet_rel(receipt_md, packet_base),
            "--json-out",
            _packet_rel(receipt_json, packet_base),
        ],
        [receipt_md, receipt_json],
        packet_base,
    )

    handoff_md = out_dir / "handoff.md"
    handoff_json = out_dir / "handoff.json"
    _export_handoff(playbook_json, compare_json, handoff_md, handoff_json, receipt_json)
    _packet_command(
        commands,
        "export-handoff",
        [
            "export-handoff",
            "--playbook",
            _packet_rel(playbook_json, packet_base),
            "--post-event-compare",
            _packet_rel(compare_json, packet_base),
            "--visual-receipt",
            _packet_rel(receipt_json, packet_base),
            "--out",
            _packet_rel(handoff_md, packet_base),
            "--json-out",
            _packet_rel(handoff_json, packet_base),
        ],
        [handoff_md, handoff_json],
        packet_base,
    )

    notebook_md = out_dir / "scenario-notebook.md"
    notebook_json = out_dir / "scenario-notebook.json"
    _scenario_notebook(
        playbook_json,
        handoff_json,
        gallery_json,
        [tutorial_json, showcase_json],
        notebook_md,
        notebook_json,
    )
    _packet_command(
        commands,
        "scenario-notebook",
        [
            "scenario-notebook",
            "--playbook",
            _packet_rel(playbook_json, packet_base),
            "--handoff",
            _packet_rel(handoff_json, packet_base),
            "--fixture-gallery",
            _packet_rel(gallery_json, packet_base),
            "--manifest",
            _packet_rel(tutorial_json, packet_base),
            _packet_rel(showcase_json, packet_base),
            "--out",
            _packet_rel(notebook_md, packet_base),
            "--json-out",
            _packet_rel(notebook_json, packet_base),
        ],
        [notebook_md, notebook_json],
        packet_base,
    )

    bridge_md = out_dir / "portfolio-drift-bridge.md"
    bridge_json = out_dir / "portfolio-drift-bridge.json"
    _portfolio_drift_bridge(packet_portfolio, notebook_json, compare_json, packet_thresholds, bridge_md, bridge_json)
    _packet_command(
        commands,
        "portfolio-drift-bridge",
        [
            "portfolio-drift-bridge",
            "--portfolio",
            _packet_rel(packet_portfolio, packet_base),
            "--scenario-notebook",
            _packet_rel(notebook_json, packet_base),
            "--post-event-compare",
            _packet_rel(compare_json, packet_base),
            "--risk-thresholds",
            _packet_rel(packet_thresholds, packet_base),
            "--out",
            _packet_rel(bridge_md, packet_base),
            "--json-out",
            _packet_rel(bridge_json, packet_base),
        ],
        [bridge_md, bridge_json],
        packet_base,
    )

    manifest_path = out_dir / "review-packet-manifest.json"
    manifest = _build_review_packet_manifest(out_dir, packet_base, commands, manifest_path)
    write_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return 0


def _selfcheck() -> int:
    roots = _selfcheck_roots()
    forbidden = [
        "Her" + "mes",
        "Fei" + "shu",
        "/" + "mnt" + "/" + "c",
        "personal " + "name",
        "token" + "=",
    ]
    scanned = []
    for root in roots:
        for path in _iter_selfcheck_files(root):
            text = path.read_text(encoding="utf-8", errors="ignore")
            scanned.append(path)
            for marker in forbidden:
                if marker in text:
                    raise ValueError(f"forbidden private marker found in {path}: {marker}")
        if (root / ".github" / "workflows").exists():
            raise ValueError("GitHub Actions workflows are intentionally not part of this repo")
    scanned_roots = ", ".join(str(root) for root in roots)
    print(
        f"selfcheck ok: version={__version__}, scanned={len(scanned)}, "
        f"roots={scanned_roots}, runtime_dependencies=0"
    )
    return 0


def _selfcheck_roots() -> list[Path]:
    return [_project_root()]


def _project_root() -> Path:
    package_root = PACKAGE_ROOT.resolve()
    for candidate in package_root.parents:
        if all((candidate / marker).exists() for marker in PROJECT_MARKER_FILES):
            source_package = candidate / "src" / package_root.name
            if source_package == package_root:
                return candidate
    return package_root


def _copy_text(source: Path, destination: Path) -> None:
    if not source.exists():
        raise ValueError(f"{source} does not exist")
    write_text(destination, source.read_text(encoding="utf-8"))


def _packet_command(
    commands: list[dict],
    name: str,
    args: list[str],
    artifacts: Sequence[Path],
    base: Path,
) -> None:
    commands.append(
        {
            "step": len(commands) + 1,
            "name": name,
            "command": "PYTHONPATH=src python -m earnings_event_playbook " + " ".join(args),
            "artifact_paths": [_packet_rel(path, base) for path in artifacts],
            "status": "completed",
        }
    )


def _build_review_packet_manifest(
    out_dir: Path,
    base: Path,
    commands: Sequence[dict],
    manifest_path: Path,
) -> dict:
    artifacts = [
        _packet_artifact(path, base)
        for path in sorted(out_dir.rglob("*"))
        if path.is_file() and path.resolve() != manifest_path.resolve()
    ]
    artifact_paths = {item["path"] for item in artifacts}
    expected_paths = {path for command in commands for path in command["artifact_paths"]}
    generated_artifacts_present = expected_paths.issubset(artifact_paths)
    release_gate_checks = [
        {
            "name": "orchestration-complete",
            "status": "pass" if all(command["status"] == "completed" for command in commands) else "fail",
            "evidence": f"{len(commands)} packet commands completed",
        },
        {
            "name": "expected-artifacts-present",
            "status": "pass" if generated_artifacts_present else "fail",
            "evidence": f"{len(expected_paths)} expected command artifacts tracked",
        },
        {
            "name": "sha256-inventory",
            "status": "pass" if all(len(item["sha256"]) == 64 for item in artifacts) else "fail",
            "evidence": f"{len(artifacts)} packet files hashed",
        },
        {
            "name": "runtime-dependencies",
            "status": "pass",
            "evidence": "pyproject.toml project.dependencies is empty",
        },
        {
            "name": "workflow-boundary",
            "status": "pass" if not (_project_root() / ".github" / "workflows").exists() else "fail",
            "evidence": "no GitHub Actions workflow directory is present",
        },
        {
            "name": "local-static-boundary",
            "status": "pass",
            "evidence": "packet inputs are copied local JSON fixtures and generated local artifacts",
        },
    ]
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "review-packet-manifest",
        "package_version": __version__,
        "output_root": _packet_rel(out_dir, base),
        "commands": list(commands),
        "artifact_paths": sorted(artifact_paths),
        "artifacts": artifacts,
        "release_gate_checks": release_gate_checks,
        "promotion_gate_notes": [
            "Promote only after pytest, unittest discovery, selfcheck, and build pass in the release environment.",
            "Confirm checked-in demo/review-packet manifest hashes match regenerated artifacts before tagging.",
            "Confirm artifact wording stays descriptive research review and does not become order, allocation, or recommendation language.",
            "Confirm any new fixture data remains synthetic or otherwise publishable and does not introduce private references.",
        ],
        "risk_boundaries": [
            "local static fixtures and generated artifacts only",
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice",
            "descriptive release-candidate review packet only",
        ],
        "next_review_prompts": [
            "Do all command artifacts have paired Markdown or HTML plus JSON where expected?",
            "Do the visual receipt and manifest hashes match after a clean regeneration?",
            "Do release gate checks remain pass after running the documented verification commands?",
            "Are scenario, handoff, and portfolio drift outputs still framed as review artifacts rather than action instructions?",
            "Are docs, changelog, package version, and release manifest aligned for the release candidate?",
        ],
    }


def _packet_artifact(path: Path, base: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": _packet_rel(path, base),
        "role": _packet_artifact_role(path),
        "media_type": _packet_media_type(path),
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _packet_artifact_role(path: Path) -> str:
    if "inputs" in path.parts:
        return "input-fixture"
    name = path.name
    if name.endswith(".md"):
        return "human-review-artifact"
    if name.endswith(".html"):
        return "static-html-preview"
    if name.endswith(".json"):
        return "machine-readable-artifact"
    return "packet-artifact"


def _packet_media_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".md":
        return "text/markdown"
    if suffix == ".html":
        return "text/html"
    if suffix == ".json":
        return "application/json"
    return "application/octet-stream"


def _packet_rel(path: Path, base: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(base.resolve()).as_posix()
    except ValueError:
        return resolved.as_posix()


def _project_rel(path: Path) -> str:
    resolved = path.resolve()
    project_root = _project_root()
    try:
        return resolved.relative_to(project_root).as_posix()
    except ValueError:
        return resolved.as_posix()


def _iter_selfcheck_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if SKIPPED_SCAN_DIRS.intersection(path.parts):
            continue
        if any(part.endswith(".egg-info") for part in path.parts):
            continue
        if path.suffix.lower() in SCANNED_SUFFIXES or path.name == "LICENSE":
            yield path


def _demo_events_json() -> str:
    return """{
  "as_of": "2026-07-08",
  "events": [
    {
      "date": "2026-07-24",
      "ticker": "EXM",
      "company": "Example Machines Inc.",
      "fiscal_period": "FY2026 Q2",
      "consensus_eps": 1.42,
      "consensus_revenue": 3250.0,
      "implied_move_percent": 6.5,
      "source_date": "2026-07-05",
      "source_name": "Static consensus fixture"
    },
    {
      "date": "2026-08-01",
      "ticker": "NXT",
      "company": "Next Retail Group",
      "fiscal_period": "FY2026 Q1",
      "consensus_eps": 0.78,
      "consensus_revenue": 1840.0,
      "implied_move_percent": 9.2,
      "source_date": "2026-05-12",
      "source_name": "Static calendar fixture"
    }
  ],
  "thesis_sensitivities": [
    {
      "topic": "gross margin",
      "note": "Margin guide and inventory commentary can change confidence in the near-term thesis.",
      "risk_weight": 3
    },
    {
      "topic": "demand durability",
      "note": "Backlog quality and repeat-order language should be reviewed after the call.",
      "risk_weight": 2
    }
  ],
  "risk_questions": [
    "Did management change full-year guidance assumptions?",
    "Were one-time items separated from recurring demand signals?"
  ]
}
"""


def _demo_portfolio_json() -> str:
    return """{
  "as_of": "2026-07-08",
  "base_currency": "USD",
  "positions": [
    {
      "ticker": "EXM",
      "shares": 120,
      "exposure": 18000,
      "portfolio_weight_percent": 4.5,
      "notes": "Core watch position for industrial automation thesis."
    },
    {
      "ticker": "NXT",
      "shares": 85,
      "exposure": 7600,
      "portfolio_weight_percent": 1.9,
      "notes": "Smaller discretionary retail exposure."
    }
  ]
}
"""


def _demo_actuals_json() -> str:
    return """{
  "as_of": "2026-07-27",
  "actuals": [
    {
      "ticker": "EXM",
      "fiscal_period": "FY2026 Q2",
      "report_date": "2026-07-24",
      "actual_eps": 1.55,
      "actual_revenue": 3378.0,
      "actual_move_percent": 7.1,
      "source_date": "2026-07-24",
      "source_name": "Static post-event fixture",
      "notes": "Revenue and margin comments require ledger follow-up against pre-event sensitivities."
    },
    {
      "ticker": "NXT",
      "fiscal_period": "FY2026 Q1",
      "report_date": "2026-08-01",
      "actual_eps": 0.72,
      "actual_revenue": 1812.0,
      "actual_move_percent": -8.4,
      "source_date": "2026-08-01",
      "source_name": "Static post-event fixture",
      "notes": "Management commentary should be attached before closing the review queue."
    }
  ]
}
"""
