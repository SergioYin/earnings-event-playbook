from __future__ import annotations

from datetime import date
from typing import List

from .models import (
    EarningsEvent,
    EventFixture,
    EventPlaybook,
    PortfolioFixture,
    ScenarioBand,
    find_position,
)


def freshness_label(as_of: date, source_date: date) -> str:
    age_days = (as_of - source_date).days
    if age_days < 0:
        return "source-after-as-of"
    if age_days <= 14:
        return "fresh<=14d"
    if age_days <= 45:
        return "watch<=45d"
    return "stale>45d"


def attention_score(event: EarningsEvent, exposure: float, sensitivity_weight: int, freshness: str) -> int:
    score = int(round(abs(event.implied_move_percent) * 2))
    if exposure:
        score += min(30, int(abs(exposure) / 1000))
    score += min(20, sensitivity_weight * 3)
    if freshness.startswith("stale"):
        score += 8
    if freshness == "source-after-as-of":
        score += 12
    return min(100, score)


def scenario_bands(event: EarningsEvent, exposure: float) -> List[ScenarioBand]:
    move = abs(event.implied_move_percent)
    specs = [
        ("beat", move, 8.0, 5.0),
        ("base", 0.0, 0.0, 0.0),
        ("miss", -move, -8.0, -5.0),
    ]
    bands = []
    for name, price_move, eps_delta, revenue_delta in specs:
        bands.append(
            ScenarioBand(
                name=name,
                price_move_percent=round(price_move, 2),
                eps_delta_percent=eps_delta,
                revenue_delta_percent=revenue_delta,
                exposure_delta=round(exposure * price_move / 100.0, 2),
                watch_items=[
                    "compare actual EPS to consensus",
                    "compare actual revenue to consensus",
                    "check guidance tone before changing thesis notes",
                ],
            )
        )
    return bands


def build_playbooks(events_fixture: EventFixture, portfolio_fixture: PortfolioFixture) -> List[EventPlaybook]:
    playbooks = []
    total_weight = sum(item.risk_weight for item in events_fixture.thesis_sensitivities)
    for event in sorted(events_fixture.events, key=lambda item: (item.date, item.ticker)):
        position = find_position(portfolio_fixture.positions, event.ticker)
        exposure = position.exposure if position else 0.0
        freshness = freshness_label(events_fixture.as_of, event.source_date)
        review_queue = [
            f"Confirm {event.ticker} report timing and source freshness before the event.",
            f"Prepare beat/base/miss notes for {event.company} {event.fiscal_period}.",
        ]
        if position is None:
            review_queue.append("No matching portfolio position; confirm whether this is watchlist-only.")
        elif position.portfolio_weight_percent >= 5:
            review_queue.append("Portfolio weight is elevated; document exposure-specific risk questions.")
        if freshness.startswith("stale") or freshness == "source-after-as-of":
            review_queue.append("Refresh static source fields before using the playbook in review.")
        review_queue.extend(events_fixture.risk_questions)

        playbooks.append(
            EventPlaybook(
                as_of=events_fixture.as_of,
                event=event,
                position=position,
                freshness=freshness,
                attention_score=attention_score(event, exposure, total_weight, freshness),
                scenario_bands=scenario_bands(event, exposure),
                thesis_sensitivities=events_fixture.thesis_sensitivities,
                risk_questions=events_fixture.risk_questions,
                review_queue=review_queue,
            )
        )
    return playbooks
