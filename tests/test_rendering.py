import json

from earnings_event_playbook.core import build_fixture_gallery, build_playbooks, compare_post_event
from earnings_event_playbook.core import build_handoff_packs
from earnings_event_playbook.models import (
    EvidenceArtifactHash,
    parse_actuals_fixture,
    parse_events_fixture,
    parse_portfolio_fixture,
)
from earnings_event_playbook.render import (
    build_scenario_notebook,
    render_fixture_gallery_json,
    render_fixture_gallery_markdown,
    render_handoff_json,
    render_handoff_markdown,
    render_html_index,
    render_json,
    render_markdown,
    render_post_event_json,
    render_post_event_markdown,
    render_scenario_notebook_json,
    render_scenario_notebook_markdown,
)


def _playbooks():
    events = parse_events_fixture(
        {
            "as_of": "2026-07-08",
            "events": [
                {
                    "date": "2026-07-24",
                    "ticker": "EXM",
                    "company": "Example Machines",
                    "fiscal_period": "Q2",
                    "consensus_eps": 1.2,
                    "consensus_revenue": 3000,
                    "implied_move_percent": 6,
                    "source_date": "2026-07-02",
                    "source_name": "Fixture",
                }
            ],
            "risk_questions": ["What changed?"],
        }
    )
    portfolio = parse_portfolio_fixture(
        {
            "as_of": "2026-07-08",
            "base_currency": "USD",
            "positions": [{"ticker": "EXM", "shares": 10, "exposure": 1000, "portfolio_weight_percent": 1}],
        }
    )
    return build_playbooks(events, portfolio)


def test_render_json_contains_boundaries():
    data = json.loads(render_json(_playbooks()))
    assert data["safety_boundaries"][0] == "local static fixtures only"
    assert data["playbooks"][0]["event"]["ticker"] == "EXM"


def test_render_fixture_gallery_compares_cases():
    events = parse_events_fixture(
        {
            "as_of": "2026-07-08",
            "events": [
                {
                    "date": "2026-08-01",
                    "ticker": "BIG",
                    "company": "Big Case",
                    "fiscal_period": "Q2",
                    "consensus_eps": 1.0,
                    "consensus_revenue": 1000,
                    "implied_move_percent": 20,
                    "source_date": "2026-04-01",
                    "source_name": "Fixture",
                }
            ],
            "thesis_sensitivities": [{"topic": "demand", "note": "Demand risk.", "risk_weight": 5}],
        }
    )
    portfolio = parse_portfolio_fixture(
        {
            "as_of": "2026-07-08",
            "base_currency": "USD",
            "positions": [{"ticker": "BIG", "shares": 10, "exposure": 50000, "portfolio_weight_percent": 12}],
        }
    )
    gallery = build_fixture_gallery([("sample", "examples/cases/sample", events, portfolio, None)])
    data = json.loads(render_fixture_gallery_json(gallery))
    markdown = render_fixture_gallery_markdown(gallery)
    assert data["artifact"] == "fixture-gallery"
    assert data["summary"]["case_count"] == 1
    assert data["cases"][0]["stale_sources"] == ["BIG:stale>45d"]
    assert data["cases"][0]["high_attention_scores"][0]["ticker"] == "BIG"
    assert data["cases"][0]["post_event_available"] is False
    assert "Fixture Case Gallery" in markdown
    assert "No actuals fixture" in markdown


def test_render_markdown_contains_review_queue():
    markdown = render_markdown(_playbooks())
    assert "# Earnings Event Playbook" in markdown
    assert "Post-Event Review Queue" in markdown


def test_render_html_has_no_script_tag():
    html = render_html_index(_playbooks())
    assert "<script" not in html.lower()
    assert "No JavaScript" in html
    assert "Risk questions" in html
    assert "Review queue" in html


def test_render_post_event_outputs_handoff_and_boundaries():
    actuals = parse_actuals_fixture(
        {
            "as_of": "2026-07-27",
            "actuals": [
                {
                    "ticker": "EXM",
                    "fiscal_period": "Q2",
                    "report_date": "2026-07-24",
                    "actual_eps": 1.3,
                    "actual_revenue": 3040,
                    "actual_move_percent": 5.5,
                    "source_date": "2026-07-24",
                    "source_name": "Fixture",
                }
            ],
        }
    )
    comparisons = compare_post_event(_playbooks(), actuals)
    data = json.loads(render_post_event_json(comparisons))
    assert data["artifact"] == "post-event-compare"
    markdown = render_post_event_markdown(comparisons)
    assert "Thesis Ledger Handoff" in markdown
    assert "Review status" in markdown


def test_render_handoff_outputs_required_fields():
    actuals = parse_actuals_fixture(
        {
            "as_of": "2026-07-27",
            "actuals": [
                {
                    "ticker": "EXM",
                    "fiscal_period": "Q2",
                    "report_date": "2026-07-24",
                    "actual_eps": 1.3,
                    "actual_revenue": 3040,
                    "actual_move_percent": 5.5,
                    "source_date": "2026-07-24",
                    "source_name": "Fixture",
                    "notes": "Call transcript needs review.",
                }
            ],
        }
    )
    comparisons = compare_post_event(_playbooks(), actuals)
    packs = build_handoff_packs(
        _playbooks(),
        comparisons,
        [
            EvidenceArtifactHash(
                path="demo/playbook.md",
                role="playbook-markdown",
                media_type="text/markdown",
                size_bytes=100,
                sha256="a" * 64,
            )
        ],
    )
    data = json.loads(render_handoff_json(packs))
    pack = data["handoff_packs"][0]
    assert data["artifact"] == "cross-asset-handoff"
    assert pack["ticker"] == "EXM"
    assert pack["fiscal_period"] == "Q2"
    assert pack["source_freshness"] == "fresh<=14d"
    assert pack["open_review_items"]
    assert pack["thesis_note_draft"]
    assert pack["risk_map_prompts"]
    assert pack["catalyst_follow_up"]
    assert pack["evidence_artifact_hashes"][0]["sha256"] == "a" * 64
    markdown = render_handoff_markdown(packs)
    assert "Cross-Asset Handoff Pack" in markdown
    assert "Earnings" not in markdown.splitlines()[0]


def test_render_scenario_notebook_combines_artifacts():
    actuals = parse_actuals_fixture(
        {
            "as_of": "2026-07-27",
            "actuals": [
                {
                    "ticker": "EXM",
                    "fiscal_period": "Q2",
                    "report_date": "2026-07-24",
                    "actual_eps": 1.3,
                    "actual_revenue": 3040,
                    "actual_move_percent": 5.5,
                    "source_date": "2026-07-24",
                    "source_name": "Fixture",
                }
            ],
        }
    )
    comparisons = compare_post_event(_playbooks(), actuals)
    packs = build_handoff_packs(
        _playbooks(),
        comparisons,
        [
            EvidenceArtifactHash(
                path="demo/playbook.md",
                role="playbook-markdown",
                media_type="text/markdown",
                size_bytes=100,
                sha256="b" * 64,
            )
        ],
    )
    gallery = build_fixture_gallery([("sample", "examples/cases/sample", parse_events_fixture({
        "as_of": "2026-07-08",
        "events": [
            {
                "date": "2026-08-01",
                "ticker": "EXM",
                "company": "Example Machines",
                "fiscal_period": "Q2",
                "consensus_eps": 1.0,
                "consensus_revenue": 1000,
                "implied_move_percent": 6,
                "source_date": "2026-07-01",
                "source_name": "Fixture",
            }
        ],
    }), parse_portfolio_fixture({
        "as_of": "2026-07-08",
        "base_currency": "USD",
        "positions": [],
    }), None)])
    notebook = build_scenario_notebook(
        json.loads(render_json(_playbooks())),
        json.loads(render_handoff_json(packs)),
        json.loads(render_fixture_gallery_json(gallery)),
        [{"artifact": "showcase-page", "title": "Showcase", "demo_artifact_links": [{"path": "demo/showcase.html"}]}],
    )
    data = json.loads(render_scenario_notebook_json(notebook))
    markdown = render_scenario_notebook_markdown(notebook)
    assert data["artifact"] == "scenario-notebook"
    assert data["summary"]["evidence_hash_count"] == 1
    assert data["optional_manifests"][0]["artifact"] == "showcase-page"
    assert data["reusable_agent_prompts"]
    assert "Scenario Reviewer Notebook" in markdown
    assert "Reusable Agent Prompts" in markdown
