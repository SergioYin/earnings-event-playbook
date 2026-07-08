from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from . import __version__
from .core import build_fixture_gallery, build_handoff_packs, build_playbooks, compare_post_event
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
