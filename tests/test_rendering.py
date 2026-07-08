import json

from earnings_event_playbook.core import build_playbooks, compare_post_event
from earnings_event_playbook.models import parse_actuals_fixture, parse_events_fixture, parse_portfolio_fixture
from earnings_event_playbook.render import render_html_index, render_json, render_markdown, render_post_event_json, render_post_event_markdown


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
