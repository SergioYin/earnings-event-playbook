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


def find_position(positions: Iterable[Position], ticker: str) -> Optional[Position]:
    target = ticker.upper()
    for position in positions:
        if position.ticker == target:
            return position
    return None
