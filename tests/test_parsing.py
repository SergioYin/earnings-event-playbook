from earnings_event_playbook.models import FixtureError, parse_events_fixture, parse_portfolio_fixture


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
