from __future__ import annotations

from datetime import date
from typing import List

from .models import (
    ActualsFixture,
    EvidenceArtifactHash,
    EarningsEvent,
    EventFixture,
    EventPlaybook,
    HandoffPack,
    MetricComparison,
    MoveComparison,
    PortfolioFixture,
    PostEventComparison,
    ScenarioBand,
    find_actual,
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


def compare_post_event(playbooks: List[EventPlaybook], actuals_fixture: ActualsFixture) -> List[PostEventComparison]:
    comparisons = []
    for playbook in playbooks:
        event = playbook.event
        actual = find_actual(actuals_fixture.actuals, event.ticker, event.fiscal_period)
        eps = _metric_comparison(
            "eps",
            event.consensus_eps,
            actual.actual_eps if actual else None,
            _scenario_thresholds(playbook.scenario_bands, "eps_delta_percent"),
        )
        revenue = _metric_comparison(
            "revenue",
            event.consensus_revenue,
            actual.actual_revenue if actual else None,
            _scenario_thresholds(playbook.scenario_bands, "revenue_delta_percent"),
        )
        move = _move_comparison(
            event.implied_move_percent,
            actual.actual_move_percent if actual else None,
            playbook.scenario_bands,
        )
        handoff = _thesis_ledger_handoff(playbook, actual, eps, revenue, move)
        review_queue = _post_event_review_queue(playbook, actual, eps, revenue, move)
        comparisons.append(
            PostEventComparison(
                as_of=actuals_fixture.as_of,
                event=event,
                actual=actual,
                eps=eps,
                revenue=revenue,
                move=move,
                review_status=_review_status(actual, eps, revenue, move),
                thesis_ledger_handoff=handoff,
                review_queue=review_queue,
            )
        )
    return comparisons


def build_handoff_packs(
    playbooks: List[EventPlaybook],
    comparisons: List[PostEventComparison],
    evidence_hashes: List[EvidenceArtifactHash] | None = None,
) -> List[HandoffPack]:
    comparison_by_key = {
        (item.event.ticker.upper(), item.event.fiscal_period.strip().lower()): item for item in comparisons
    }
    hashes = evidence_hashes or []
    packs = []
    for playbook in playbooks:
        event = playbook.event
        comparison = comparison_by_key.get((event.ticker.upper(), event.fiscal_period.strip().lower()))
        if comparison is None:
            open_items = [f"Add post-event comparison for {event.ticker} {event.fiscal_period}."]
            open_items.extend(playbook.review_queue)
            packs.append(
                HandoffPack(
                    ticker=event.ticker,
                    company=event.company,
                    fiscal_period=event.fiscal_period,
                    source_freshness=playbook.freshness,
                    event_source_name=event.source_name,
                    event_source_date=event.source_date,
                    actual_source_name="not matched",
                    actual_source_date=None,
                    review_status="blocked-missing-comparison",
                    open_review_items=open_items,
                    thesis_note_draft=_missing_comparison_thesis_note(playbook),
                    risk_map_prompts=_risk_map_prompts(playbook, None),
                    catalyst_follow_up=_catalyst_follow_up(playbook, None),
                    evidence_artifact_hashes=hashes,
                )
            )
            continue

        open_items = _open_handoff_items(playbook, comparison)
        packs.append(
            HandoffPack(
                ticker=event.ticker,
                company=event.company,
                fiscal_period=event.fiscal_period,
                source_freshness=playbook.freshness,
                event_source_name=event.source_name,
                event_source_date=event.source_date,
                actual_source_name=comparison.actual.source_name if comparison.actual else "not matched",
                actual_source_date=comparison.actual.source_date if comparison.actual else None,
                review_status=comparison.review_status,
                open_review_items=open_items,
                thesis_note_draft=_thesis_note_draft(playbook, comparison),
                risk_map_prompts=_risk_map_prompts(playbook, comparison),
                catalyst_follow_up=_catalyst_follow_up(playbook, comparison),
                evidence_artifact_hashes=hashes,
            )
        )
    return packs


def _scenario_thresholds(bands: List[ScenarioBand], attr: str) -> dict:
    thresholds = {band.name: getattr(band, attr) for band in bands}
    return {
        "beat": float(thresholds.get("beat", 8.0)),
        "miss": float(thresholds.get("miss", -8.0)),
    }


def _metric_comparison(metric: str, consensus: float | None, actual: float | None, thresholds: dict) -> MetricComparison:
    if consensus is None or actual is None:
        return MetricComparison(metric, consensus, actual, None, None, "not-comparable")
    delta = actual - consensus
    delta_percent = 0.0 if consensus == 0 else (delta / abs(consensus)) * 100.0
    if delta_percent >= thresholds["beat"]:
        band = "beat"
    elif delta_percent <= thresholds["miss"]:
        band = "miss"
    else:
        band = "base"
    return MetricComparison(metric, consensus, actual, round(delta, 4), round(delta_percent, 2), band)


def _move_comparison(
    implied_move_percent: float, actual_move_percent: float | None, bands: List[ScenarioBand]
) -> MoveComparison:
    if actual_move_percent is None:
        return MoveComparison(implied_move_percent, None, None, "not-comparable")
    if bands:
        matched = min(bands, key=lambda band: abs(band.price_move_percent - actual_move_percent)).name
    else:
        matched = "base"
    return MoveComparison(
        implied_move_percent=implied_move_percent,
        actual_move_percent=actual_move_percent,
        delta_percent=round(actual_move_percent - implied_move_percent, 2),
        matched_scenario=matched,
    )


def _thesis_ledger_handoff(
    playbook: EventPlaybook,
    actual,
    eps: MetricComparison,
    revenue: MetricComparison,
    move: MoveComparison,
) -> List[str]:
    event = playbook.event
    if actual is None:
        return [f"{event.ticker}: no matching actuals fixture; keep pre-event thesis ledger open for data capture."]

    notes = [
        f"{event.ticker} {event.fiscal_period}: EPS classified as {eps.band}; revenue classified as {revenue.band}; post-event move matched {move.matched_scenario}.",
        f"Source handoff: {actual.source_name} dated {actual.source_date.isoformat()}; report date {actual.report_date.isoformat()}.",
    ]
    if actual.notes:
        notes.append(f"Actuals note for ledger: {actual.notes}")
    if playbook.thesis_sensitivities:
        topics = ", ".join(item.topic for item in playbook.thesis_sensitivities)
        notes.append(f"Review thesis sensitivity topics before closing ledger: {topics}.")
    else:
        notes.append("No thesis sensitivity topics were provided in the before-playbook.")
    return notes


def _post_event_review_queue(
    playbook: EventPlaybook,
    actual,
    eps: MetricComparison,
    revenue: MetricComparison,
    move: MoveComparison,
) -> List[str]:
    event = playbook.event
    queue = [f"Attach actuals source for {event.ticker} {event.fiscal_period} to the thesis ledger."]
    if actual is None:
        queue.append("Add a matching actuals fixture entry before marking the review complete.")
        return queue
    for comparison in (eps, revenue):
        if comparison.band == "not-comparable":
            queue.append(f"Fill missing {comparison.metric} consensus or actual value for comparison.")
    if move.matched_scenario == "not-comparable":
        queue.append("Fill missing post-event move value for scenario comparison.")
    if eps.band != revenue.band and "not-comparable" not in {eps.band, revenue.band}:
        queue.append("EPS and revenue landed in different bands; document which thesis sensitivity changed.")
    if move.matched_scenario not in {eps.band, revenue.band, "not-comparable"}:
        queue.append("Price move scenario differs from fundamentals bands; add market-reaction context.")
    queue.extend(f"Answer after-call question: {question}" for question in playbook.risk_questions)
    if len(queue) == 1:
        queue.append("No additional comparison exceptions detected; complete source review and archive notes.")
    return queue


def _review_status(actual, eps: MetricComparison, revenue: MetricComparison, move: MoveComparison) -> str:
    if actual is None:
        return "blocked-missing-actuals"
    if "not-comparable" in {eps.band, revenue.band, move.matched_scenario}:
        return "needs-data"
    if eps.band != revenue.band or move.matched_scenario not in {eps.band, revenue.band}:
        return "needs-review"
    return "ready-for-ledger"


def _open_handoff_items(playbook: EventPlaybook, comparison: PostEventComparison) -> List[str]:
    items = list(comparison.review_queue)
    if playbook.freshness.startswith("stale") or playbook.freshness == "source-after-as-of":
        items.append(f"Refresh source freshness for {playbook.event.ticker} before closing handoff.")
    if not items:
        items.append("Archive source links and mark the local review complete.")
    return items


def _thesis_note_draft(playbook: EventPlaybook, comparison: PostEventComparison) -> str:
    event = playbook.event
    actual_source = "not matched" if comparison.actual is None else comparison.actual.source_name
    return (
        f"{event.ticker} {event.fiscal_period} handoff: review status {comparison.review_status}. "
        f"EPS band {comparison.eps.band}; revenue band {comparison.revenue.band}; "
        f"post-event move matched {comparison.move.matched_scenario}. "
        f"Pre-event source freshness was {playbook.freshness}; actuals source was {actual_source}. "
        "Use this as a thesis-ledger draft note after source review; it is not an action recommendation."
    )


def _missing_comparison_thesis_note(playbook: EventPlaybook) -> str:
    event = playbook.event
    return (
        f"{event.ticker} {event.fiscal_period} handoff is blocked because no post-event comparison matched. "
        f"Pre-event source freshness was {playbook.freshness}. Add actuals comparison evidence before closing."
    )


def _risk_map_prompts(playbook: EventPlaybook, comparison: PostEventComparison | None) -> List[str]:
    event = playbook.event
    prompts = [
        f"Map {event.ticker} {event.fiscal_period} source freshness ({playbook.freshness}) to the call-risk log.",
        "Identify which thesis sensitivities need updated evidence after the earnings call.",
    ]
    prompts.extend(f"Call-risk prompt: {question}" for question in playbook.risk_questions)
    if comparison is not None:
        prompts.append(
            f"Compare EPS band {comparison.eps.band}, revenue band {comparison.revenue.band}, "
            f"and move scenario {comparison.move.matched_scenario} for divergence."
        )
    return prompts


def _catalyst_follow_up(playbook: EventPlaybook, comparison: PostEventComparison | None) -> List[str]:
    event = playbook.event
    follow_up = [
        f"Carry forward unresolved {event.ticker} {event.fiscal_period} review items into the next catalyst log.",
        "Attach source artifacts and notes before marking the event review closed.",
    ]
    if comparison is None or comparison.actual is None:
        follow_up.append("Add matched actuals evidence before catalyst follow-up is complete.")
    elif comparison.actual.notes:
        follow_up.append(f"Review actuals note for catalyst context: {comparison.actual.notes}")
    if playbook.thesis_sensitivities:
        topics = ", ".join(item.topic for item in playbook.thesis_sensitivities)
        follow_up.append(f"Update thesis sensitivity evidence for: {topics}.")
    return follow_up
