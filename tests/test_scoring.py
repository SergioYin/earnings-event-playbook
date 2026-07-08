from earnings_event_playbook.core import build_playbooks, freshness_label, scenario_bands
from earnings_event_playbook.models import parse_events_fixture, parse_portfolio_fixture


def test_freshness_label_buckets():
    assert freshness_label(__import__("datetime").date(2026, 7, 8), __import__("datetime").date(2026, 7, 1)) == "fresh<=14d"
    assert freshness_label(__import__("datetime").date(2026, 7, 8), __import__("datetime").date(2026, 5, 1)) == "stale>45d"


def test_scenario_bands_are_deterministic():
    event = parse_events_fixture(
        {
            "as_of": "2026-07-08",
            "events": [
                {
                    "date": "2026-07-24",
                    "ticker": "EXM",
                    "company": "Example Machines",
                    "fiscal_period": "Q2",
                    "implied_move_percent": 6.5,
                    "source_date": "2026-07-02",
                    "source_name": "Fixture",
                }
            ],
        }
    ).events[0]
    bands = scenario_bands(event, 10000)
    assert [band.name for band in bands] == ["beat", "base", "miss"]
    assert bands[0].exposure_delta == 650.0
    assert bands[2].exposure_delta == -650.0


def test_build_playbooks_adds_review_queue_for_missing_position():
    events = parse_events_fixture(
        {
            "as_of": "2026-07-08",
            "events": [
                {
                    "date": "2026-07-24",
                    "ticker": "EXM",
                    "company": "Example Machines",
                    "fiscal_period": "Q2",
                    "implied_move_percent": 6.5,
                    "source_date": "2026-07-02",
                    "source_name": "Fixture",
                }
            ],
        }
    )
    portfolio = parse_portfolio_fixture({"as_of": "2026-07-08", "base_currency": "USD", "positions": []})
    playbook = build_playbooks(events, portfolio)[0]
    assert "watchlist-only" in " ".join(playbook.review_queue)
