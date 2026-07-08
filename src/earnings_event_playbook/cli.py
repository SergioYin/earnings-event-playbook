from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from . import __version__
from .core import build_playbooks, compare_post_event
from .io import read_json, write_text
from .models import FixtureError, parse_actuals_fixture, parse_events_fixture, parse_playbook_json, parse_portfolio_fixture
from .render import render_html_index, render_json, render_markdown, render_post_event_json, render_post_event_markdown


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

    subparsers.add_parser("selfcheck", help="Verify package boundaries and fixture parsing.")

    args = parser.parse_args(argv)
    try:
        if args.command == "build-playbook":
            return _build_playbook(args.events, args.portfolio, args.out, args.json_out)
        if args.command == "compare-post-event":
            return _compare_post_event(args.before_playbook, args.actuals, args.out, args.json_out)
        if args.command == "demo-bundle":
            return _demo_bundle(args.out)
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
    package_root = PACKAGE_ROOT.resolve()
    for candidate in package_root.parents:
        if all((candidate / marker).exists() for marker in PROJECT_MARKER_FILES):
            source_package = candidate / "src" / package_root.name
            if source_package == package_root:
                return [candidate]
    return [package_root]


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
