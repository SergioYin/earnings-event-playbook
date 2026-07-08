from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, Iterable, List, Mapping, Optional


class FixtureError(ValueError):
    """Raised when a local fixture is missing required public fields."""


def parse_date(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise FixtureError(f"{field_name} must be an ISO date string") from exc


def require_text(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise FixtureError(f"{key} is required")
    return value.strip()


def number_or_none(data: Mapping[str, Any], key: str) -> Optional[float]:
    value = data.get(key)
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    raise FixtureError(f"{key} must be a number when provided")


def list_of_text(data: Mapping[str, Any], key: str) -> List[str]:
    value = data.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise FixtureError(f"{key} must be a list of strings")
    return [item.strip() for item in value if item.strip()]


@dataclass(frozen=True)
class EarningsEvent:
    date: date
    ticker: str
    company: str
    fiscal_period: str
    consensus_eps: Optional[float]
    consensus_revenue: Optional[float]
    implied_move_percent: float
    source_date: date
    source_name: str


@dataclass(frozen=True)
class Position:
    ticker: str
    shares: float
    exposure: float
    portfolio_weight_percent: float
    notes: str = ""


@dataclass(frozen=True)
class ThesisSensitivity:
    topic: str
    note: str
    risk_weight: int = 1


@dataclass(frozen=True)
class EventFixture:
    as_of: date
    events: List[EarningsEvent]
    thesis_sensitivities: List[ThesisSensitivity]
    risk_questions: List[str]


@dataclass(frozen=True)
class PortfolioFixture:
    as_of: date
    base_currency: str
    positions: List[Position]


@dataclass(frozen=True)
class ScenarioBand:
    name: str
    price_move_percent: float
    eps_delta_percent: float
    revenue_delta_percent: float
    exposure_delta: float
    watch_items: List[str]


@dataclass(frozen=True)
class ActualOutcome:
    ticker: str
    fiscal_period: str
    report_date: date
    actual_eps: Optional[float]
    actual_revenue: Optional[float]
    actual_move_percent: Optional[float]
    source_name: str
    source_date: date
    notes: str = ""


@dataclass(frozen=True)
class ActualsFixture:
    as_of: date
    actuals: List[ActualOutcome]


@dataclass(frozen=True)
class MetricComparison:
    metric: str
    consensus: Optional[float]
    actual: Optional[float]
    delta: Optional[float]
    delta_percent: Optional[float]
    band: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric,
            "consensus": self.consensus,
            "actual": self.actual,
            "delta": self.delta,
            "delta_percent": self.delta_percent,
            "band": self.band,
        }


@dataclass(frozen=True)
class MoveComparison:
    implied_move_percent: float
    actual_move_percent: Optional[float]
    delta_percent: Optional[float]
    matched_scenario: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "implied_move_percent": self.implied_move_percent,
            "actual_move_percent": self.actual_move_percent,
            "delta_percent": self.delta_percent,
            "matched_scenario": self.matched_scenario,
        }


@dataclass(frozen=True)
class PostEventComparison:
    as_of: date
    event: EarningsEvent
    actual: Optional[ActualOutcome]
    eps: MetricComparison
    revenue: MetricComparison
    move: MoveComparison
    review_status: str
    thesis_ledger_handoff: List[str]
    review_queue: List[str]
    safety_notice: str = (
        "Educational post-event review only. Uses local static fixtures only; "
        "no live data, broker connection, orders, or investment advice."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "as_of": self.as_of.isoformat(),
            "event": {
                "date": self.event.date.isoformat(),
                "ticker": self.event.ticker,
                "company": self.event.company,
                "fiscal_period": self.event.fiscal_period,
                "consensus_eps": self.event.consensus_eps,
                "consensus_revenue": self.event.consensus_revenue,
                "implied_move_percent": self.event.implied_move_percent,
                "source_date": self.event.source_date.isoformat(),
                "source_name": self.event.source_name,
            },
            "actual": None
            if self.actual is None
            else {
                "ticker": self.actual.ticker,
                "fiscal_period": self.actual.fiscal_period,
                "report_date": self.actual.report_date.isoformat(),
                "actual_eps": self.actual.actual_eps,
                "actual_revenue": self.actual.actual_revenue,
                "actual_move_percent": self.actual.actual_move_percent,
                "source_name": self.actual.source_name,
                "source_date": self.actual.source_date.isoformat(),
                "notes": self.actual.notes,
            },
            "eps": self.eps.to_dict(),
            "revenue": self.revenue.to_dict(),
            "move": self.move.to_dict(),
            "review_status": self.review_status,
            "thesis_ledger_handoff": list(self.thesis_ledger_handoff),
            "review_queue": list(self.review_queue),
            "safety_notice": self.safety_notice,
        }


@dataclass(frozen=True)
class EvidenceArtifactHash:
    path: str
    role: str
    media_type: str
    size_bytes: int
    sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path": self.path,
            "role": self.role,
            "media_type": self.media_type,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class HandoffPack:
    ticker: str
    company: str
    fiscal_period: str
    source_freshness: str
    event_source_name: str
    event_source_date: date
    actual_source_name: str
    actual_source_date: Optional[date]
    review_status: str
    open_review_items: List[str]
    thesis_note_draft: str
    risk_map_prompts: List[str]
    catalyst_follow_up: List[str]
    evidence_artifact_hashes: List[EvidenceArtifactHash] = field(default_factory=list)
    safety_notice: str = (
        "Educational cross-asset research handoff only. Uses local static artifacts only; "
        "no live data, broker connection, orders, or investment advice."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ticker": self.ticker,
            "company": self.company,
            "fiscal_period": self.fiscal_period,
            "source_freshness": self.source_freshness,
            "event_source": {
                "name": self.event_source_name,
                "date": self.event_source_date.isoformat(),
            },
            "actual_source": {
                "name": self.actual_source_name,
                "date": None if self.actual_source_date is None else self.actual_source_date.isoformat(),
            },
            "review_status": self.review_status,
            "open_review_items": list(self.open_review_items),
            "thesis_note_draft": self.thesis_note_draft,
            "risk_map_prompts": list(self.risk_map_prompts),
            "catalyst_follow_up": list(self.catalyst_follow_up),
            "evidence_artifact_hashes": [item.to_dict() for item in self.evidence_artifact_hashes],
            "safety_notice": self.safety_notice,
        }


@dataclass(frozen=True)
class EventPlaybook:
    as_of: date
    event: EarningsEvent
    position: Optional[Position]
    freshness: str
    attention_score: int
    scenario_bands: List[ScenarioBand]
    thesis_sensitivities: List[ThesisSensitivity]
    risk_questions: List[str]
    review_queue: List[str]
    safety_notice: str = (
        "Educational research review only. Uses local static fixtures only; "
        "no live data, broker connection, orders, or investment advice."
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "as_of": self.as_of.isoformat(),
            "event": {
                "date": self.event.date.isoformat(),
                "ticker": self.event.ticker,
                "company": self.event.company,
                "fiscal_period": self.event.fiscal_period,
                "consensus_eps": self.event.consensus_eps,
                "consensus_revenue": self.event.consensus_revenue,
                "implied_move_percent": self.event.implied_move_percent,
                "source_date": self.event.source_date.isoformat(),
                "source_name": self.event.source_name,
            },
            "position": None
            if self.position is None
            else {
                "ticker": self.position.ticker,
                "shares": self.position.shares,
                "exposure": self.position.exposure,
                "portfolio_weight_percent": self.position.portfolio_weight_percent,
                "notes": self.position.notes,
            },
            "freshness": self.freshness,
            "attention_score": self.attention_score,
            "scenario_bands": [
                {
                    "name": band.name,
                    "price_move_percent": band.price_move_percent,
                    "eps_delta_percent": band.eps_delta_percent,
                    "revenue_delta_percent": band.revenue_delta_percent,
                    "exposure_delta": band.exposure_delta,
                    "watch_items": list(band.watch_items),
                }
                for band in self.scenario_bands
            ],
            "thesis_sensitivities": [
                {
                    "topic": item.topic,
                    "note": item.note,
                    "risk_weight": item.risk_weight,
                }
                for item in self.thesis_sensitivities
            ],
            "risk_questions": list(self.risk_questions),
            "review_queue": list(self.review_queue),
            "safety_notice": self.safety_notice,
        }


def parse_events_fixture(raw: Mapping[str, Any]) -> EventFixture:
    as_of = parse_date(require_text(raw, "as_of"), "as_of")
    events_raw = raw.get("events")
    if not isinstance(events_raw, list) or not events_raw:
        raise FixtureError("events must be a non-empty list")

    events = []
    for index, item in enumerate(events_raw):
        if not isinstance(item, Mapping):
            raise FixtureError(f"events[{index}] must be an object")
        events.append(
            EarningsEvent(
                date=parse_date(require_text(item, "date"), f"events[{index}].date"),
                ticker=require_text(item, "ticker").upper(),
                company=require_text(item, "company"),
                fiscal_period=require_text(item, "fiscal_period"),
                consensus_eps=number_or_none(item, "consensus_eps"),
                consensus_revenue=number_or_none(item, "consensus_revenue"),
                implied_move_percent=float(number_or_none(item, "implied_move_percent") or 0.0),
                source_date=parse_date(require_text(item, "source_date"), f"events[{index}].source_date"),
                source_name=require_text(item, "source_name"),
            )
        )

    sensitivity_raw = raw.get("thesis_sensitivities", [])
    if not isinstance(sensitivity_raw, list):
        raise FixtureError("thesis_sensitivities must be a list")
    sensitivities = []
    for index, item in enumerate(sensitivity_raw):
        if not isinstance(item, Mapping):
            raise FixtureError(f"thesis_sensitivities[{index}] must be an object")
        weight = item.get("risk_weight", 1)
        if not isinstance(weight, int):
            raise FixtureError(f"thesis_sensitivities[{index}].risk_weight must be an integer")
        sensitivities.append(
            ThesisSensitivity(
                topic=require_text(item, "topic"),
                note=require_text(item, "note"),
                risk_weight=max(1, weight),
            )
        )

    return EventFixture(
        as_of=as_of,
        events=events,
        thesis_sensitivities=sensitivities,
        risk_questions=list_of_text(raw, "risk_questions"),
    )


def parse_portfolio_fixture(raw: Mapping[str, Any]) -> PortfolioFixture:
    as_of = parse_date(require_text(raw, "as_of"), "as_of")
    positions_raw = raw.get("positions")
    if not isinstance(positions_raw, list):
        raise FixtureError("positions must be a list")

    positions = []
    for index, item in enumerate(positions_raw):
        if not isinstance(item, Mapping):
            raise FixtureError(f"positions[{index}] must be an object")
        positions.append(
            Position(
                ticker=require_text(item, "ticker").upper(),
                shares=float(number_or_none(item, "shares") or 0.0),
                exposure=float(number_or_none(item, "exposure") or 0.0),
                portfolio_weight_percent=float(number_or_none(item, "portfolio_weight_percent") or 0.0),
                notes=str(item.get("notes", "")).strip(),
            )
        )

    return PortfolioFixture(
        as_of=as_of,
        base_currency=require_text(raw, "base_currency"),
        positions=positions,
    )


def parse_actuals_fixture(raw: Mapping[str, Any]) -> ActualsFixture:
    as_of = parse_date(require_text(raw, "as_of"), "as_of")
    actuals_raw = raw.get("actuals")
    if not isinstance(actuals_raw, list) or not actuals_raw:
        raise FixtureError("actuals must be a non-empty list")

    actuals = []
    for index, item in enumerate(actuals_raw):
        if not isinstance(item, Mapping):
            raise FixtureError(f"actuals[{index}] must be an object")
        actuals.append(
            ActualOutcome(
                ticker=require_text(item, "ticker").upper(),
                fiscal_period=require_text(item, "fiscal_period"),
                report_date=parse_date(require_text(item, "report_date"), f"actuals[{index}].report_date"),
                actual_eps=number_or_none(item, "actual_eps"),
                actual_revenue=number_or_none(item, "actual_revenue"),
                actual_move_percent=number_or_none(item, "actual_move_percent"),
                source_name=require_text(item, "source_name"),
                source_date=parse_date(require_text(item, "source_date"), f"actuals[{index}].source_date"),
                notes=str(item.get("notes", "")).strip(),
            )
        )
    return ActualsFixture(as_of=as_of, actuals=actuals)


def parse_playbook_json(raw: Any) -> List[EventPlaybook]:
    if isinstance(raw, Mapping) and isinstance(raw.get("playbooks"), list):
        items = raw["playbooks"]
    elif isinstance(raw, Mapping) and isinstance(raw.get("event"), Mapping):
        items = [raw]
    elif isinstance(raw, list):
        items = raw
    else:
        raise FixtureError("before-playbook must be rendered playbook JSON or a playbook object")

    playbooks = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise FixtureError(f"playbooks[{index}] must be an object")
        event_raw = item.get("event")
        if not isinstance(event_raw, Mapping):
            raise FixtureError(f"playbooks[{index}].event is required")
        position_raw = item.get("position")
        if position_raw is not None and not isinstance(position_raw, Mapping):
            raise FixtureError(f"playbooks[{index}].position must be an object or null")
        bands_raw = item.get("scenario_bands", [])
        if not isinstance(bands_raw, list):
            raise FixtureError(f"playbooks[{index}].scenario_bands must be a list")
        sensitivities_raw = item.get("thesis_sensitivities", [])
        if not isinstance(sensitivities_raw, list):
            raise FixtureError(f"playbooks[{index}].thesis_sensitivities must be a list")

        playbooks.append(
            EventPlaybook(
                as_of=parse_date(require_text(item, "as_of"), f"playbooks[{index}].as_of"),
                event=EarningsEvent(
                    date=parse_date(require_text(event_raw, "date"), f"playbooks[{index}].event.date"),
                    ticker=require_text(event_raw, "ticker").upper(),
                    company=require_text(event_raw, "company"),
                    fiscal_period=require_text(event_raw, "fiscal_period"),
                    consensus_eps=number_or_none(event_raw, "consensus_eps"),
                    consensus_revenue=number_or_none(event_raw, "consensus_revenue"),
                    implied_move_percent=float(number_or_none(event_raw, "implied_move_percent") or 0.0),
                    source_date=parse_date(
                        require_text(event_raw, "source_date"), f"playbooks[{index}].event.source_date"
                    ),
                    source_name=require_text(event_raw, "source_name"),
                ),
                position=None
                if position_raw is None
                else Position(
                    ticker=require_text(position_raw, "ticker").upper(),
                    shares=float(number_or_none(position_raw, "shares") or 0.0),
                    exposure=float(number_or_none(position_raw, "exposure") or 0.0),
                    portfolio_weight_percent=float(number_or_none(position_raw, "portfolio_weight_percent") or 0.0),
                    notes=str(position_raw.get("notes", "")).strip(),
                ),
                freshness=require_text(item, "freshness"),
                attention_score=int(number_or_none(item, "attention_score") or 0),
                scenario_bands=[_parse_scenario_band(band, index, band_index) for band_index, band in enumerate(bands_raw)],
                thesis_sensitivities=[
                    _parse_thesis_sensitivity(sensitivity, index, sensitivity_index)
                    for sensitivity_index, sensitivity in enumerate(sensitivities_raw)
                ],
                risk_questions=list_of_text(item, "risk_questions"),
                review_queue=list_of_text(item, "review_queue"),
                safety_notice=str(item.get("safety_notice", "")).strip() or EventPlaybook.safety_notice,
            )
        )
    return playbooks


def parse_post_event_compare_json(raw: Any) -> List[PostEventComparison]:
    if isinstance(raw, Mapping) and isinstance(raw.get("comparisons"), list):
        items = raw["comparisons"]
    elif isinstance(raw, Mapping) and isinstance(raw.get("event"), Mapping):
        items = [raw]
    elif isinstance(raw, list):
        items = raw
    else:
        raise FixtureError("post-event-compare must be rendered comparison JSON or a comparison object")

    comparisons = []
    for index, item in enumerate(items):
        if not isinstance(item, Mapping):
            raise FixtureError(f"comparisons[{index}] must be an object")
        event_raw = item.get("event")
        if not isinstance(event_raw, Mapping):
            raise FixtureError(f"comparisons[{index}].event is required")
        actual_raw = item.get("actual")
        if actual_raw is not None and not isinstance(actual_raw, Mapping):
            raise FixtureError(f"comparisons[{index}].actual must be an object or null")
        comparisons.append(
            PostEventComparison(
                as_of=parse_date(require_text(item, "as_of"), f"comparisons[{index}].as_of"),
                event=EarningsEvent(
                    date=parse_date(require_text(event_raw, "date"), f"comparisons[{index}].event.date"),
                    ticker=require_text(event_raw, "ticker").upper(),
                    company=require_text(event_raw, "company"),
                    fiscal_period=require_text(event_raw, "fiscal_period"),
                    consensus_eps=number_or_none(event_raw, "consensus_eps"),
                    consensus_revenue=number_or_none(event_raw, "consensus_revenue"),
                    implied_move_percent=float(number_or_none(event_raw, "implied_move_percent") or 0.0),
                    source_date=parse_date(
                        require_text(event_raw, "source_date"), f"comparisons[{index}].event.source_date"
                    ),
                    source_name=require_text(event_raw, "source_name"),
                ),
                actual=None
                if actual_raw is None
                else ActualOutcome(
                    ticker=require_text(actual_raw, "ticker").upper(),
                    fiscal_period=require_text(actual_raw, "fiscal_period"),
                    report_date=parse_date(
                        require_text(actual_raw, "report_date"), f"comparisons[{index}].actual.report_date"
                    ),
                    actual_eps=number_or_none(actual_raw, "actual_eps"),
                    actual_revenue=number_or_none(actual_raw, "actual_revenue"),
                    actual_move_percent=number_or_none(actual_raw, "actual_move_percent"),
                    source_name=require_text(actual_raw, "source_name"),
                    source_date=parse_date(
                        require_text(actual_raw, "source_date"), f"comparisons[{index}].actual.source_date"
                    ),
                    notes=str(actual_raw.get("notes", "")).strip(),
                ),
                eps=_parse_metric_comparison(item.get("eps"), index, "eps"),
                revenue=_parse_metric_comparison(item.get("revenue"), index, "revenue"),
                move=_parse_move_comparison(item.get("move"), index),
                review_status=require_text(item, "review_status"),
                thesis_ledger_handoff=list_of_text(item, "thesis_ledger_handoff"),
                review_queue=list_of_text(item, "review_queue"),
                safety_notice=str(item.get("safety_notice", "")).strip() or PostEventComparison.safety_notice,
            )
        )
    return comparisons


def parse_visual_receipt_hashes(raw: Mapping[str, Any]) -> List[EvidenceArtifactHash]:
    files_raw = raw.get("files", [])
    if not isinstance(files_raw, list):
        raise FixtureError("visual receipt files must be a list")
    hashes = []
    for index, item in enumerate(files_raw):
        if not isinstance(item, Mapping):
            raise FixtureError(f"visual receipt files[{index}] must be an object")
        size = item.get("size_bytes")
        if not isinstance(size, int):
            raise FixtureError(f"visual receipt files[{index}].size_bytes must be an integer")
        hashes.append(
            EvidenceArtifactHash(
                path=require_text(item, "path"),
                role=require_text(item, "role"),
                media_type=require_text(item, "media_type"),
                size_bytes=size,
                sha256=require_text(item, "sha256"),
            )
        )
    return hashes


def _parse_metric_comparison(raw: Any, comparison_index: int, key: str) -> MetricComparison:
    if not isinstance(raw, Mapping):
        raise FixtureError(f"comparisons[{comparison_index}].{key} must be an object")
    return MetricComparison(
        metric=require_text(raw, "metric"),
        consensus=number_or_none(raw, "consensus"),
        actual=number_or_none(raw, "actual"),
        delta=number_or_none(raw, "delta"),
        delta_percent=number_or_none(raw, "delta_percent"),
        band=require_text(raw, "band"),
    )


def _parse_move_comparison(raw: Any, comparison_index: int) -> MoveComparison:
    if not isinstance(raw, Mapping):
        raise FixtureError(f"comparisons[{comparison_index}].move must be an object")
    return MoveComparison(
        implied_move_percent=float(number_or_none(raw, "implied_move_percent") or 0.0),
        actual_move_percent=number_or_none(raw, "actual_move_percent"),
        delta_percent=number_or_none(raw, "delta_percent"),
        matched_scenario=require_text(raw, "matched_scenario"),
    )


def _parse_scenario_band(raw: Any, playbook_index: int, band_index: int) -> ScenarioBand:
    if not isinstance(raw, Mapping):
        raise FixtureError(f"playbooks[{playbook_index}].scenario_bands[{band_index}] must be an object")
    return ScenarioBand(
        name=require_text(raw, "name"),
        price_move_percent=float(number_or_none(raw, "price_move_percent") or 0.0),
        eps_delta_percent=float(number_or_none(raw, "eps_delta_percent") or 0.0),
        revenue_delta_percent=float(number_or_none(raw, "revenue_delta_percent") or 0.0),
        exposure_delta=float(number_or_none(raw, "exposure_delta") or 0.0),
        watch_items=list_of_text(raw, "watch_items"),
    )


def _parse_thesis_sensitivity(raw: Any, playbook_index: int, sensitivity_index: int) -> ThesisSensitivity:
    if not isinstance(raw, Mapping):
        raise FixtureError(f"playbooks[{playbook_index}].thesis_sensitivities[{sensitivity_index}] must be an object")
    weight = raw.get("risk_weight", 1)
    if not isinstance(weight, int):
        raise FixtureError(
            f"playbooks[{playbook_index}].thesis_sensitivities[{sensitivity_index}].risk_weight must be an integer"
        )
    return ThesisSensitivity(topic=require_text(raw, "topic"), note=require_text(raw, "note"), risk_weight=max(1, weight))


def find_position(positions: Iterable[Position], ticker: str) -> Optional[Position]:
    target = ticker.upper()
    for position in positions:
        if position.ticker == target:
            return position
    return None


def find_actual(actuals: Iterable[ActualOutcome], ticker: str, fiscal_period: str) -> Optional[ActualOutcome]:
    target_ticker = ticker.upper()
    target_period = fiscal_period.strip().lower()
    for actual in actuals:
        if actual.ticker == target_ticker and actual.fiscal_period.strip().lower() == target_period:
            return actual
    return None
