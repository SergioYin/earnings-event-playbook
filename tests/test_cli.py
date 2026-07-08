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
    assert (tmp_path / "showcase.html").exists()
    assert (tmp_path / "showcase.json").exists()
    assert (tmp_path / "visual-receipt.md").exists()
    assert (tmp_path / "visual-receipt.json").exists()
    assert (tmp_path / "handoff.md").exists()
    assert (tmp_path / "handoff.json").exists()
    assert (tmp_path / "fixture-gallery.md").exists()
    assert (tmp_path / "fixture-gallery.json").exists()
    assert (tmp_path / "tutorial-bundle.md").exists()
    assert (tmp_path / "tutorial-bundle.json").exists()
    assert (tmp_path / "scenario-notebook.md").exists()
    assert (tmp_path / "scenario-notebook.json").exists()
    assert (tmp_path / "portfolio-drift-bridge.md").exists()
    assert (tmp_path / "portfolio-drift-bridge.json").exists()
    data = json.loads((tmp_path / "playbook.json").read_text(encoding="utf-8"))
    assert data["generated_by"] == "earnings-event-playbook"
    receipt = json.loads((tmp_path / "visual-receipt.json").read_text(encoding="utf-8"))
    assert receipt["artifact"] == "visual-receipt"
    assert receipt["summary"]["file_count"] == 10
    assert receipt["summary"]["roles"]["html-artifact"] == 1
    handoff = json.loads((tmp_path / "handoff.json").read_text(encoding="utf-8"))
    assert handoff["artifact"] == "cross-asset-handoff"
    assert handoff["handoff_packs"][0]["evidence_artifact_hashes"]
    notebook = json.loads((tmp_path / "scenario-notebook.json").read_text(encoding="utf-8"))
    assert notebook["artifact"] == "scenario-notebook"
    assert notebook["summary"]["optional_manifest_count"] == 2
    bridge = json.loads((tmp_path / "portfolio-drift-bridge.json").read_text(encoding="utf-8"))
    assert bridge["artifact"] == "portfolio-drift-bridge"
    assert bridge["summary"]["event_linked_ticker_count"] == 2


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


def test_cli_fixture_gallery(tmp_path):
    out = tmp_path / "fixture-gallery.md"
    json_out = tmp_path / "fixture-gallery.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "fixture-gallery",
            "--cases",
            "examples/cases/software",
            "examples/cases/retail",
            "examples/cases/semiconductor",
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
    assert "Fixture Case Gallery" in text
    assert data["artifact"] == "fixture-gallery"
    assert data["summary"]["case_count"] == 3
    assert data["summary"]["event_count"] == 7
    assert data["summary"]["post_event_case_count"] == 2
    assert data["cases"][0]["case_id"] == "retail"
    assert data["cases"][0]["post_event_available"] is False
    assert all("fixture-gallery" not in command for case in data["cases"] for command in case["supported_demo_commands"])


def test_cli_tutorial_bundle(tmp_path):
    out = tmp_path / "tutorial-bundle.md"
    json_out = tmp_path / "tutorial-bundle.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "tutorial-bundle",
            "--case",
            "examples/cases/software",
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
    assert "Tutorial Bundle: software" in text
    assert data["artifact"] == "tutorial-bundle"
    assert data["case_id"] == "software"
    assert data["tutorial_article"] == "docs/tutorial-software-case.md"
    assert [item["step"] for item in data["ordered_commands"]] == [1, 2, 3, 4, 5]
    assert data["ordered_commands"][0]["expected_artifacts"] == [
        "demo/cases/software/playbook.md",
        "demo/cases/software/playbook.json",
    ]
    assert "compare-post-event" in data["ordered_commands"][1]["command"]
    assert "visual-receipt" in data["ordered_commands"][2]["command"]
    assert "export-handoff" in data["ordered_commands"][3]["command"]
    assert "fixture-gallery" in data["ordered_commands"][4]["command"]
    assert data["reviewer_checklist"]
    assert data["maturity_rubric_evidence"]
    assert any("no broker connection" == item for item in data["safety_boundaries"])


def test_cli_showcase_page(tmp_path):
    out = tmp_path / "showcase.html"
    json_out = tmp_path / "showcase.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "showcase-page",
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
    assert "Earnings Event Playbook Showcase" in text
    assert "<script" not in text.lower()
    assert data["artifact"] == "showcase-page"
    assert data["quickstart_commands"][1].startswith("PYTHONPATH=src python -m earnings_event_playbook showcase-page")
    assert any(item["path"] == "demo/showcase.html" for item in data["demo_artifact_links"])
    assert data["release_evidence"]
    assert data["maturity_rubric"]
    assert data["case_gallery_highlights"]
    assert data["tutorial_path"]
    assert data["risk_boundaries"]
    assert data["star_worthy_differentiation"]
    assert all("financial advice" not in item.lower() for item in data["star_worthy_differentiation"])


def test_cli_scenario_notebook(tmp_path):
    subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "demo-bundle", "--out", str(tmp_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    out = tmp_path / "notebook.md"
    json_out = tmp_path / "notebook.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "scenario-notebook",
            "--playbook",
            str(tmp_path / "playbook.json"),
            "--handoff",
            str(tmp_path / "handoff.json"),
            "--fixture-gallery",
            str(tmp_path / "fixture-gallery.json"),
            "--manifest",
            str(tmp_path / "tutorial-bundle.json"),
            str(tmp_path / "showcase.json"),
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
    assert "Scenario Reviewer Notebook" in text
    assert "Thesis Assumptions" in text
    assert "Scenario Bands" in text
    assert "Source Freshness" in text
    assert "Evidence Hashes" in text
    assert "Comparison Aftermath" in text
    assert "Next-Action Queue" in text
    assert "Risk Boundary Checklist" in text
    assert "Reusable Agent Prompts" in text
    assert data["artifact"] == "scenario-notebook"
    assert data["summary"]["playbook_count"] == 2
    assert data["summary"]["handoff_pack_count"] == 2
    assert data["summary"]["case_count"] == 3
    assert data["summary"]["optional_manifest_count"] == 2
    assert data["thesis_assumptions"]
    assert data["scenario_bands"][0]["bands"]
    assert data["source_freshness"]
    assert data["evidence_hashes"]
    assert data["comparison_aftermath"]
    assert data["next_action_queue"]
    assert data["risk_boundary_checklist"]
    assert data["reusable_agent_prompts"]


def test_cli_portfolio_drift_bridge(tmp_path):
    subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "demo-bundle", "--out", str(tmp_path)],
        check=True,
        text=True,
        capture_output=True,
    )
    out = tmp_path / "bridge-rerun.md"
    json_out = tmp_path / "bridge-rerun.json"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "earnings_event_playbook",
            "portfolio-drift-bridge",
            "--portfolio",
            str(tmp_path / "portfolio.json"),
            "--scenario-notebook",
            str(tmp_path / "scenario-notebook.json"),
            "--post-event-compare",
            str(tmp_path / "post-event-compare.json"),
            "--risk-thresholds",
            "examples/risk-thresholds.json",
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
    assert "Portfolio Drift Bridge" in text
    assert data["artifact"] == "portfolio-drift-bridge"
    assert data["inputs"]["threshold_source"] == "provided-static-json"
    assert data["exposure_concentration"][0]["ticker"] == "EXM"
    assert data["scenario_mismatch_alerts"]
    assert data["post_event_drift_watchlist"]
    assert data["no_trade_safety_boundaries"]


def test_cli_review_packet_manifest_schema_and_roles(tmp_path):
    out_dir = tmp_path / "review-packet"
    subprocess.run(
        [sys.executable, "-m", "earnings_event_playbook", "review-packet", "--out", str(out_dir)],
        check=True,
        text=True,
        capture_output=True,
    )
    manifest = json.loads((out_dir / "review-packet-manifest.json").read_text(encoding="utf-8"))
    assert manifest["schema_version"] == "1.0"
    assert manifest["artifact"] == "review-packet-manifest"
    assert manifest["generated_by"] == "earnings-event-playbook"
    assert manifest["package_version"] == "1.1.0"
    assert manifest["output_root"] == "review-packet"
    assert [command["step"] for command in manifest["commands"]] == list(range(1, 10))
    assert all(command["status"] == "completed" for command in manifest["commands"])
    assert all(check["status"] == "pass" for check in manifest["release_gate_checks"])
    assert len(manifest["artifacts"]) == 22
    assert sorted(item["path"] for item in manifest["artifacts"]) == manifest["artifact_paths"]
    assert all(len(item["sha256"]) == 64 for item in manifest["artifacts"])
    roles = {item["path"]: item["role"] for item in manifest["artifacts"]}
    assert roles["review-packet/playbook.json"] == "pre-event-playbook-artifact"
    assert roles["review-packet/post-event-compare.json"] == "post-event-comparison-artifact"
    assert roles["review-packet/visual-receipt.json"] == "hash-receipt-artifact"
    assert roles["review-packet/showcase.html"] == "showcase-artifact"
    assert roles["review-packet/inputs/events.json"] == "input-fixture"
    expected_paths = {path for command in manifest["commands"] for path in command["artifact_paths"]}
    assert expected_paths.issubset(set(manifest["artifact_paths"]))


def test_cli_review_packet_manifest_is_deterministic_and_public(tmp_path):
    first = tmp_path / "first" / "review-packet"
    second = tmp_path / "second" / "review-packet"
    for out_dir in [first, second]:
        subprocess.run(
            [sys.executable, "-m", "earnings_event_playbook", "review-packet", "--out", str(out_dir)],
            check=True,
            text=True,
            capture_output=True,
        )

    first_text = (first / "review-packet-manifest.json").read_text(encoding="utf-8")
    second_text = (second / "review-packet-manifest.json").read_text(encoding="utf-8")
    assert first_text == second_text

    manifest = json.loads(first_text)
    all_strings = json.dumps(manifest, sort_keys=True)
    assert str(tmp_path) not in all_strings
    assert not any(Path(item["path"]).is_absolute() for item in manifest["artifacts"])
    assert not any(Path(path).is_absolute() for path in manifest["artifact_paths"])
    assert not any(".." in Path(item["path"]).parts for item in manifest["artifacts"])
    private_markers = ["Her" + "mes", "Fei" + "shu", "/" + "home" + "/" + "xjyin", "/" + "mnt" + "/" + "c"]
    assert not any(marker in all_strings for marker in private_markers)


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
    assert not any(item["path"].endswith("scenario-notebook.json") for item in data["files"])


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
