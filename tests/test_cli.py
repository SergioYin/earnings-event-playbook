import json
import re
import os
import subprocess
import sys
from pathlib import Path


def test_cli_demo_bundle(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "demo-bundle", "--out", str(tmp_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert (tmp_path / "playbook.md").exists()
    assert (tmp_path / "playbook.json").exists()
    assert (tmp_path / "index.html").exists()
    assert (tmp_path / "visual-receipt.md").exists()
    assert (tmp_path / "visual-receipt.json").exists()
    assert (tmp_path / "handoff.md").exists()
    assert (tmp_path / "handoff.json").exists()
    data = json.loads((tmp_path / "playbook.json").read_text(encoding="utf-8"))
    assert data["generated_by"] == "earnings-event-playbook"
    receipt = json.loads((tmp_path / "visual-receipt.json").read_text(encoding="utf-8"))
    assert receipt["artifact"] == "visual-receipt"
    assert receipt["summary"]["file_count"] == 8
    handoff = json.loads((tmp_path / "handoff.json").read_text(encoding="utf-8"))
    assert handoff["artifact"] == "cross-asset-handoff"
    assert handoff["handoff_packs"][0]["evidence_artifact_hashes"]


def test_cli_build_playbook(tmp_path):
    out = tmp_path / "playbook.md"
    json_out = tmp_path / "playbook.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "build-playbook",
            "--events",
            "examples/events.json",
            "--portfolio",
            "examples/portfolio.json",
            "--out",
            str(out),
            "--json-out",
            str(json_out),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "Earnings Event Playbook" in out.read_text(encoding="utf-8")
    assert json.loads(json_out.read_text(encoding="utf-8"))["playbooks"]


def test_cli_compare_post_event(tmp_path):
    playbook_json = tmp_path / "playbook.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "build-playbook",
            "--events",
            "examples/events.json",
            "--portfolio",
            "examples/portfolio.json",
            "--out",
            str(tmp_path / "playbook.md"),
            "--json-out",
            str(playbook_json),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    out = tmp_path / "post-event.md"
    json_out = tmp_path / "post-event.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "compare-post-event",
            "--before-playbook",
            str(playbook_json),
            "--actuals",
            "examples/actuals.json",
            "--out",
            str(out),
            "--json-out",
            str(json_out),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    assert "Post-Event Compare" in out.read_text(encoding="utf-8")
    data = json.loads(json_out.read_text(encoding="utf-8"))
    assert data["artifact"] == "post-event-compare"
    assert data["comparisons"][0]["thesis_ledger_handoff"]


def test_cli_visual_receipt(tmp_path):
    subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "demo-bundle", "--out", str(tmp_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    out = tmp_path / "receipt.md"
    json_out = tmp_path / "receipt.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "visual-receipt",
            "--artifacts",
            str(tmp_path),
            "--out",
            str(out),
            "--json-out",
            str(json_out),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    text = out.read_text(encoding="utf-8")
    data = json.loads(json_out.read_text(encoding="utf-8"))
    assert "Visual Evidence Receipt" in text
    assert data["summary"]["roles"]["static-html-preview"] == 1
    assert data["summary"]["roles"]["input-fixture"] == 3
    assert all(len(item["sha256"]) == 64 for item in data["files"])
    assert not any(item["path"].endswith("visual-receipt.json") for item in data["files"])
    assert not any(item["path"].endswith("handoff.json") for item in data["files"])


def test_cli_export_handoff(tmp_path):
    subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "demo-bundle", "--out", str(tmp_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    out = tmp_path / "handoff-rerun.md"
    json_out = tmp_path / "handoff-rerun.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "export-handoff",
            "--playbook",
            str(tmp_path / "playbook.json"),
            "--post-event-compare",
            str(tmp_path / "post-event-compare.json"),
            "--visual-receipt",
            str(tmp_path / "visual-receipt.json"),
            "--out",
            str(out),
            "--json-out",
            str(json_out),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    text = out.read_text(encoding="utf-8")
    data = json.loads(json_out.read_text(encoding="utf-8"))
    pack = data["handoff_packs"][0]
    assert "Cross-Asset Handoff Pack" in text
    assert data["workflows"] == ["thesis-ledger", "earnings-call-risk-map"]
    assert pack["ticker"] == "EXM"
    assert pack["fiscal_period"] == "FY2026 Q2"
    assert pack["source_freshness"] == "fresh<=14d"
    assert pack["open_review_items"]
    assert pack["thesis_note_draft"]
    assert pack["risk_map_prompts"]
    assert pack["catalyst_follow_up"]
    assert all(len(item["sha256"]) == 64 for item in pack["evidence_artifact_hashes"])


def test_cli_selfcheck_scans_package_boundaries_from_other_cwd(tmp_path):
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "selfcheck"],
        check=True,
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert "selfcheck ok" in result.stdout
    match = re.search(r"scanned=(\d+)", result.stdout)
    assert match is not None
    assert int(match.group(1)) > 0
