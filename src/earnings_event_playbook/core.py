from __future__ import annotations

from datetime import date
from typing import Any, Mapping, List

from .models import (
    ActualsFixture,
    CaseGallery,
    CaseGalleryItem,
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


GALLERY_SAFETY_BOUNDARIES = [
    "local static fixtures only",
    "no live market data",
    "no broker connection",
    "no order placement",
    "no personalized investment advice",
]

HIGH_ATTENTION_THRESHOLD = 70

PORTFOLIO_DRIFT_BRIDGE_SAFETY_BOUNDARIES = [
    "local static fixtures and generated artifacts only",
    "no live market data",
    "no broker connection",
    "no order placement",
    "no personalized investment, legal, tax, accounting, buy, sell, hold, allocation, or other financial advice",
    "descriptive portfolio drift review only",
]

PORTFOLIO_DRIFT_BRIDGE_NO_TRADE_BOUNDARIES = [
    "Do not treat concentration flags as trade instructions.",
    "Do not convert scenario mismatch alerts into buy, sell, hold, hedge, rebalance, or allocation actions.",
    "Do not place, route, stage, or simulate orders from this packet.",
    "Do not use this packet without independent source review and suitability review outside this package.",
]

DEFAULT_PORTFOLIO_DRIFT_THRESHOLDS = {
    "max_position_weight_percent": 5.0,
    "max_exposure_share_percent": 35.0,
    "post_event_move_watch_percent": 6.0,
    "post_event_exposure_drift_amount": 1000.0,
    "max_open_review_items": 6,
}


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


def build_fixture_gallery(case_inputs: List[tuple[str, str, EventFixture, PortfolioFixture, ActualsFixture | None]]) -> CaseGallery:
    cases = []
    for case_id, case_path, events_fixture, portfolio_fixture, actuals_fixture in sorted(
        case_inputs, key=lambda item: item[0]
    ):
        playbooks = build_playbooks(events_fixture, portfolio_fixture)
        actuals = actuals_fixture.actuals if actuals_fixture is not None else []
        commands = [
            (
                "PYTHONPATH=src python -m earnings_event_playbook build-playbook "
                f"--events {case_path}/events.json --portfolio {case_path}/portfolio.json "
                f"--out demo/cases/{case_id}/playbook.md --json-out demo/cases/{case_id}/playbook.json"
            )
        ]
        if actuals_fixture is not None:
            commands.append(
                (
                    "PYTHONPATH=src python -m earnings_event_playbook compare-post-event "
                    f"--before-playbook demo/cases/{case_id}/playbook.json --actuals {case_path}/actuals.json "
                    f"--out demo/cases/{case_id}/post-event-compare.md "
                    f"--json-out demo/cases/{case_id}/post-event-compare.json"
                )
            )
        cases.append(
            CaseGalleryItem(
                case_id=case_id,
                case_path=case_path,
                tickers=sorted({item.event.ticker for item in playbooks}),
                event_count=len(playbooks),
                stale_sources=[
                    f"{item.event.ticker}:{item.freshness}"
                    for item in playbooks
                    if item.freshness.startswith("stale") or item.freshness == "source-after-as-of"
                ],
                high_attention_scores=[
                    {
                        "ticker": item.event.ticker,
                        "score": item.attention_score,
                        "fiscal_period": item.event.fiscal_period,
                    }
                    for item in playbooks
                    if item.attention_score >= HIGH_ATTENTION_THRESHOLD
                ],
                post_event_available=actuals_fixture is not None,
                post_event_match_count=sum(
                    1 for item in playbooks if find_actual(actuals, item.event.ticker, item.event.fiscal_period)
                ),
                supported_demo_commands=commands,
                safety_boundaries=GALLERY_SAFETY_BOUNDARIES,
            )
        )

    common_root = _common_case_root([item[1] for item in case_inputs])
    return CaseGallery(cases_root=common_root, cases=cases, safety_boundaries=GALLERY_SAFETY_BOUNDARIES)


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


def _common_case_root(case_paths: List[str]) -> str:
    if not case_paths:
        return ""
    split_paths = [path.strip("/").split("/") for path in case_paths]
    common = []
    for parts in zip(*split_paths):
        if len(set(parts)) != 1:
            break
        common.append(parts[0])
    return "/".join(common)


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


def build_portfolio_drift_bridge(
    portfolio_fixture: PortfolioFixture,
    scenario_notebook: Mapping[str, Any],
    post_event_compare: Mapping[str, Any],
    thresholds: Mapping[str, Any] | None = None,
) -> dict:
    threshold_values = _portfolio_drift_thresholds(thresholds)
    positions = sorted(portfolio_fixture.positions, key=lambda item: abs(item.exposure), reverse=True)
    total_abs_exposure = sum(abs(item.exposure) for item in positions)
    event_tickers = _bridge_event_tickers(scenario_notebook, post_event_compare)
    comparisons = list(post_event_compare.get("comparisons", []))
    comparison_by_ticker = {
        str(item.get("event", {}).get("ticker", "")).upper(): item for item in comparisons if isinstance(item, Mapping)
    }

    exposure_concentration = [
        _bridge_concentration_item(position, total_abs_exposure, event_tickers, threshold_values)
        for position in positions
    ]
    event_linked_tickers = [
        _bridge_event_linked_ticker(
            ticker,
            scenario_notebook,
            comparison_by_ticker.get(ticker),
            next((item for item in exposure_concentration if item["ticker"] == ticker), None),
        )
        for ticker in event_tickers
    ]
    mismatch_alerts = _bridge_scenario_mismatch_alerts(comparisons)
    drift_watchlist = _bridge_post_event_drift_watchlist(
        comparisons,
        {item.ticker: item for item in portfolio_fixture.positions},
        threshold_values,
    )
    next_prompts = _bridge_next_review_prompts(
        scenario_notebook, event_linked_tickers, mismatch_alerts, drift_watchlist, threshold_values
    )

    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "portfolio-drift-bridge",
        "inputs": {
            "portfolio_as_of": portfolio_fixture.as_of.isoformat(),
            "portfolio_base_currency": portfolio_fixture.base_currency,
            "scenario_notebook_artifact": scenario_notebook.get("artifact", "scenario-notebook"),
            "post_event_compare_artifact": post_event_compare.get("artifact", "post-event-compare"),
            "threshold_source": "provided-static-json" if thresholds else "defaults",
        },
        "thresholds": threshold_values,
        "summary": {
            "position_count": len(positions),
            "event_linked_ticker_count": len(event_linked_tickers),
            "scenario_mismatch_alert_count": len(mismatch_alerts),
            "post_event_drift_watch_count": len(drift_watchlist),
            "total_abs_exposure": round(total_abs_exposure, 2),
            "top_exposure_ticker": positions[0].ticker if positions else "",
        },
        "exposure_concentration": exposure_concentration,
        "event_linked_tickers": event_linked_tickers,
        "scenario_mismatch_alerts": mismatch_alerts,
        "post_event_drift_watchlist": drift_watchlist,
        "next_risk_review_prompts": next_prompts,
        "no_trade_safety_boundaries": PORTFOLIO_DRIFT_BRIDGE_NO_TRADE_BOUNDARIES,
        "safety_boundaries": PORTFOLIO_DRIFT_BRIDGE_SAFETY_BOUNDARIES,
    }


def _portfolio_drift_thresholds(thresholds: Mapping[str, Any] | None) -> dict:
    values = dict(DEFAULT_PORTFOLIO_DRIFT_THRESHOLDS)
    if thresholds is None:
        return values
    raw = thresholds.get("thresholds", thresholds)
    if not isinstance(raw, Mapping):
        raise ValueError("risk threshold JSON must be an object or contain a thresholds object")
    for key in values:
        if key not in raw:
            continue
        value = raw[key]
        if not isinstance(value, (int, float)):
            raise ValueError(f"risk threshold {key} must be numeric")
        values[key] = float(value)
    values["max_open_review_items"] = int(values["max_open_review_items"])
    return values


def _bridge_event_tickers(scenario_notebook: Mapping[str, Any], post_event_compare: Mapping[str, Any]) -> List[str]:
    tickers = {
        str(item.get("ticker", "")).upper()
        for item in scenario_notebook.get("thesis_assumptions", [])
        if isinstance(item, Mapping) and item.get("ticker")
    }
    tickers.update(
        str(item.get("ticker", "")).upper()
        for item in scenario_notebook.get("scenario_bands", [])
        if isinstance(item, Mapping) and item.get("ticker")
    )
    tickers.update(
        str(item.get("event", {}).get("ticker", "")).upper()
        for item in post_event_compare.get("comparisons", [])
        if isinstance(item, Mapping) and isinstance(item.get("event"), Mapping) and item.get("event", {}).get("ticker")
    )
    return sorted(tickers)


def _bridge_concentration_item(
    position: Position,
    total_abs_exposure: float,
    event_tickers: List[str],
    thresholds: Mapping[str, Any],
) -> dict:
    exposure_share = 0.0 if total_abs_exposure == 0 else abs(position.exposure) / total_abs_exposure * 100.0
    flags = []
    if position.portfolio_weight_percent >= thresholds["max_position_weight_percent"]:
        flags.append("weight-threshold")
    if exposure_share >= thresholds["max_exposure_share_percent"]:
        flags.append("exposure-share-threshold")
    if position.ticker in event_tickers:
        flags.append("event-linked")
    return {
        "ticker": position.ticker,
        "shares": position.shares,
        "exposure": round(position.exposure, 2),
        "portfolio_weight_percent": round(position.portfolio_weight_percent, 2),
        "exposure_share_percent": round(exposure_share, 2),
        "event_linked": position.ticker in event_tickers,
        "flags": flags,
        "notes": position.notes,
    }


def _bridge_event_linked_ticker(
    ticker: str,
    scenario_notebook: Mapping[str, Any],
    comparison: Mapping[str, Any] | None,
    concentration: Mapping[str, Any] | None,
) -> dict:
    assumption = next(
        (
            item
            for item in scenario_notebook.get("thesis_assumptions", [])
            if isinstance(item, Mapping) and str(item.get("ticker", "")).upper() == ticker
        ),
        {},
    )
    freshness = next(
        (
            item
            for item in scenario_notebook.get("source_freshness", [])
            if isinstance(item, Mapping) and str(item.get("ticker", "")).upper() == ticker
        ),
        {},
    )
    event_raw = comparison.get("event", {}) if isinstance(comparison, Mapping) else {}
    return {
        "ticker": ticker,
        "company": assumption.get("company", event_raw.get("company", "")),
        "fiscal_period": assumption.get("fiscal_period", event_raw.get("fiscal_period", "")),
        "portfolio_weight_percent": concentration.get("portfolio_weight_percent", 0.0) if concentration else 0.0,
        "exposure": concentration.get("exposure", 0.0) if concentration else 0.0,
        "source_freshness": freshness.get("freshness", ""),
        "review_status": comparison.get("review_status", "missing-post-event-compare") if comparison else "missing-post-event-compare",
        "risk_questions": list(assumption.get("risk_questions", [])) if isinstance(assumption, Mapping) else [],
    }


def _bridge_scenario_mismatch_alerts(comparisons: List[Any]) -> List[dict]:
    alerts = []
    for item in comparisons:
        if not isinstance(item, Mapping):
            continue
        event = item.get("event", {})
        ticker = str(event.get("ticker", "")).upper() if isinstance(event, Mapping) else ""
        fiscal_period = str(event.get("fiscal_period", "")) if isinstance(event, Mapping) else ""
        eps_band = str(item.get("eps", {}).get("band", "not-comparable"))
        revenue_band = str(item.get("revenue", {}).get("band", "not-comparable"))
        move_band = str(item.get("move", {}).get("matched_scenario", "not-comparable"))
        reasons = []
        if "not-comparable" in {eps_band, revenue_band, move_band}:
            reasons.append("comparison-not-comparable")
        if eps_band != revenue_band and "not-comparable" not in {eps_band, revenue_band}:
            reasons.append("eps-revenue-band-divergence")
        if move_band not in {eps_band, revenue_band, "not-comparable"}:
            reasons.append("move-fundamental-band-divergence")
        if item.get("review_status") not in {"ready-for-ledger", "complete"}:
            reasons.append(f"review-status:{item.get('review_status', 'missing')}")
        if reasons:
            alerts.append(
                {
                    "ticker": ticker,
                    "fiscal_period": fiscal_period,
                    "eps_band": eps_band,
                    "revenue_band": revenue_band,
                    "move_scenario": move_band,
                    "review_status": item.get("review_status", ""),
                    "reasons": reasons,
                }
            )
    return alerts


def _bridge_post_event_drift_watchlist(
    comparisons: List[Any],
    positions_by_ticker: Mapping[str, Position],
    thresholds: Mapping[str, Any],
) -> List[dict]:
    watchlist = []
    for item in comparisons:
        if not isinstance(item, Mapping):
            continue
        event = item.get("event", {})
        ticker = str(event.get("ticker", "")).upper() if isinstance(event, Mapping) else ""
        position = positions_by_ticker.get(ticker)
        move = item.get("move", {})
        actual_move = move.get("actual_move_percent") if isinstance(move, Mapping) else None
        if not isinstance(actual_move, (int, float)):
            continue
        exposure = position.exposure if position else 0.0
        estimated_drift = round(exposure * float(actual_move) / 100.0, 2)
        triggers = []
        if abs(float(actual_move)) >= thresholds["post_event_move_watch_percent"]:
            triggers.append("move-threshold")
        if abs(estimated_drift) >= thresholds["post_event_exposure_drift_amount"]:
            triggers.append("exposure-drift-threshold")
        if triggers:
            watchlist.append(
                {
                    "ticker": ticker,
                    "fiscal_period": event.get("fiscal_period", "") if isinstance(event, Mapping) else "",
                    "actual_move_percent": round(float(actual_move), 2),
                    "position_exposure": round(exposure, 2),
                    "estimated_exposure_drift": estimated_drift,
                    "matched_scenario": move.get("matched_scenario", "") if isinstance(move, Mapping) else "",
                    "triggers": triggers,
                    "review_status": item.get("review_status", ""),
                }
            )
    return watchlist


def _bridge_next_review_prompts(
    scenario_notebook: Mapping[str, Any],
    event_linked_tickers: List[dict],
    mismatch_alerts: List[dict],
    drift_watchlist: List[dict],
    thresholds: Mapping[str, Any],
) -> List[str]:
    prompts = []
    for alert in mismatch_alerts:
        prompts.append(
            f"Review {alert['ticker']} {alert['fiscal_period']} mismatch reasons before closing the event packet: {', '.join(alert['reasons'])}."
        )
    for item in drift_watchlist:
        prompts.append(
            f"Check {item['ticker']} post-event drift evidence against portfolio exposure and source notes before the next risk review."
        )
    for item in event_linked_tickers:
        if item["risk_questions"]:
            prompts.append(f"Carry forward {item['ticker']} risk questions: {'; '.join(item['risk_questions'])}")
    queue_items = [item for item in scenario_notebook.get("next_action_queue", []) if isinstance(item, Mapping)]
    max_queue_items = int(thresholds["max_open_review_items"])
    if len(queue_items) > max_queue_items:
        prompts.append(
            f"Notebook has {len(queue_items)} open review items; triage before the next risk review packet is archived."
        )
    for item in queue_items[:max_queue_items]:
        if isinstance(item, Mapping) and item.get("item"):
            prompts.append(f"Open notebook queue item for {item.get('ticker', '')}: {item['item']}")
    if not prompts:
        prompts.append("Confirm source attachments, review status, and no-trade boundaries before archiving the packet.")
    deduped = []
    for prompt in prompts:
        if prompt not in deduped:
            deduped.append(prompt)
    return deduped


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
