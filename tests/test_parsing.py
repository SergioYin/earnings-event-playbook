from earnings_event_playbook.models import (
    FixtureError,
    parse_actuals_fixture,
    parse_events_fixture,
    parse_portfolio_fixture,
    parse_post_event_compare_json,
    parse_visual_receipt_hashes,
)


def test_parse_events_fixture_requires_events():
    try:
        parse_events_fixture({"as_of": "2026-07-08", "events": []})
    except FixtureError:
        return
    raise AssertionError("expected FixtureError")


def test_parse_events_fixture_normalizes_ticker():
    fixture = parse_events_fixture(
        {
            "as_of": "2026-07-08",
            "events": [
                {
                    "date": "2026-07-24",
                    "ticker": "exm",
                    "company": "Example Machines",
                    "fiscal_period": "FY2026 Q2",
                    "implied_move_percent": 5,
                    "source_date": "2026-07-01",
                    "source_name": "Fixture",
                }
            ],
        }
    )
    assert fixture.events[0].ticker == "EXM"


def test_parse_portfolio_fixture_accepts_empty_positions():
    fixture = parse_portfolio_fixture({"as_of": "2026-07-08", "base_currency": "USD", "positions": []})
    assert fixture.positions == []


def test_parse_actuals_fixture_normalizes_ticker():
    fixture = parse_actuals_fixture(
        {
            "as_of": "2026-07-27",
            "actuals": [
                {
                    "ticker": "exm",
                    "fiscal_period": "FY2026 Q2",
                    "report_date": "2026-07-24",
                    "actual_eps": 1.55,
                    "actual_revenue": 3378,
                    "actual_move_percent": 7.1,
                    "source_date": "2026-07-24",
                    "source_name": "Fixture",
                }
            ],
        }
    )
    assert fixture.actuals[0].ticker == "EXM"


def test_parse_post_event_compare_json_accepts_rendered_shape():
    comparisons = parse_post_event_compare_json(
        {
            "comparisons": [
                {
                    "as_of": "2026-07-27",
                    "event": {
                        "date": "2026-07-24",
                        "ticker": "exm",
                        "company": "Example Machines",
                        "fiscal_period": "FY2026 Q2",
                        "consensus_eps": 1.2,
                        "consensus_revenue": 3000,
                        "implied_move_percent": 6,
                        "source_date": "2026-07-02",
                        "source_name": "Fixture",
                    },
                    "actual": None,
                    "eps": {
                        "metric": "eps",
                        "consensus": 1.2,
                        "actual": None,
                        "delta": None,
                        "delta_percent": None,
                        "band": "not-comparable",
                    },
                    "revenue": {
                        "metric": "revenue",
                        "consensus": 3000,
                        "actual": None,
                        "delta": None,
                        "delta_percent": None,
                        "band": "not-comparable",
                    },
                    "move": {
                        "implied_move_percent": 6,
                        "actual_move_percent": None,
                        "delta_percent": None,
                        "matched_scenario": "not-comparable",
                    },
                    "review_status": "needs-data",
                    "thesis_ledger_handoff": ["Keep ledger open."],
                    "review_queue": ["Attach source."],
                }
            ]
        }
    )
    assert comparisons[0].event.ticker == "EXM"
    assert comparisons[0].review_queue == ["Attach source."]


def test_parse_visual_receipt_hashes_accepts_file_inventory():
    hashes = parse_visual_receipt_hashes(
        {
            "files": [
                {
                    "path": "demo/playbook.md",
                    "role": "playbook-markdown",
                    "media_type": "text/markdown",
                    "size_bytes": 123,
                    "sha256": "b" * 64,
                }
            ]
        }
    )
    assert hashes[0].path == "demo/playbook.md"
    assert hashes[0].sha256 == "b" * 64
