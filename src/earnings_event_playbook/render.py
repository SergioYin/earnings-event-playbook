from __future__ import annotations

import html
import json
from typing import Iterable, List

from .models import EventPlaybook, PostEventComparison


def playbooks_to_dict(playbooks: Iterable[EventPlaybook]) -> dict:
    items = [item.to_dict() for item in playbooks]
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "safety_boundaries": [
            "local static fixtures only",
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment advice",
        ],
        "playbooks": items,
    }


def render_json(playbooks: Iterable[EventPlaybook]) -> str:
    return json.dumps(playbooks_to_dict(playbooks), indent=2, sort_keys=True) + "\n"


def post_event_to_dict(comparisons: Iterable[PostEventComparison]) -> dict:
    items = [item.to_dict() for item in comparisons]
    return {
        "schema_version": "1.0",
        "generated_by": "earnings-event-playbook",
        "artifact": "post-event-compare",
        "safety_boundaries": [
            "local static fixtures only",
            "no live market data",
            "no broker connection",
            "no order placement",
            "no personalized investment advice",
        ],
        "comparisons": items,
    }


def render_post_event_json(comparisons: Iterable[PostEventComparison]) -> str:
    return json.dumps(post_event_to_dict(comparisons), indent=2, sort_keys=True) + "\n"


def render_markdown(playbooks: Iterable[EventPlaybook]) -> str:
    items = list(playbooks)
    lines: List[str] = [
        "# Earnings Event Playbook",
        "",
        "> Educational research review only. Local static fixtures only; no live data, broker connection, orders, or investment advice.",
        "",
        "## Summary",
        "",
        f"- Events: {len(items)}",
        f"- Review queue items: {sum(len(item.review_queue) for item in items)}",
        "",
    ]
    for item in items:
        event = item.event
        lines.extend(
            [
                f"## {event.ticker} - {event.company}",
                "",
                f"- Event date: {event.date.isoformat()}",
                f"- Fiscal period: {event.fiscal_period}",
                f"- Consensus EPS: {_fmt_number(event.consensus_eps)}",
                f"- Consensus revenue: {_fmt_number(event.consensus_revenue)}",
                f"- Implied move: {event.implied_move_percent:.2f}%",
                f"- Source: {event.source_name} ({event.source_date.isoformat()}, {item.freshness})",
                f"- Attention score: {item.attention_score}/100",
                "",
                "### Position",
                "",
            ]
        )
        if item.position is None:
            lines.append("- No matching portfolio position in fixture.")
        else:
            position = item.position
            lines.extend(
                [
                    f"- Shares: {position.shares:g}",
                    f"- Exposure: {position.exposure:.2f}",
                    f"- Portfolio weight: {position.portfolio_weight_percent:.2f}%",
                    f"- Notes: {position.notes or 'None'}",
                ]
            )
        lines.extend(["", "### Scenario Bands", "", "| Scenario | Price move | EPS delta | Revenue delta | Exposure delta |", "| --- | ---: | ---: | ---: | ---: |"])
        for band in item.scenario_bands:
            lines.append(
                f"| {band.name} | {band.price_move_percent:.2f}% | {band.eps_delta_percent:.2f}% | "
                f"{band.revenue_delta_percent:.2f}% | {band.exposure_delta:.2f} |"
            )
        lines.extend(["", "### Thesis Sensitivities", ""])
        if item.thesis_sensitivities:
            for sensitivity in item.thesis_sensitivities:
                lines.append(f"- **{sensitivity.topic}** ({sensitivity.risk_weight}): {sensitivity.note}")
        else:
            lines.append("- None provided.")
        lines.extend(["", "### Risk Questions", ""])
        if item.risk_questions:
            lines.extend(f"- {question}" for question in item.risk_questions)
        else:
            lines.append("- None provided.")
        lines.extend(["", "### Post-Event Review Queue", ""])
        lines.extend(f"- {entry}" for entry in item.review_queue)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_post_event_markdown(comparisons: Iterable[PostEventComparison]) -> str:
    items = list(comparisons)
    lines: List[str] = [
        "# Post-Event Compare",
        "",
        "> Educational research review only. Local static fixtures only; no live data, broker connection, orders, or investment advice.",
        "",
        "## Summary",
        "",
        f"- Comparisons: {len(items)}",
        f"- Review queue items: {sum(len(item.review_queue) for item in items)}",
        "",
    ]
    for item in items:
        event = item.event
        lines.extend(
            [
                f"## {event.ticker} - {event.company}",
                "",
                f"- Fiscal period: {event.fiscal_period}",
                f"- Event date: {event.date.isoformat()}",
                f"- Review status: {item.review_status}",
            ]
        )
        if item.actual is None:
            lines.append("- Actuals source: not matched")
        else:
            actual = item.actual
            lines.extend(
                [
                    f"- Report date: {actual.report_date.isoformat()}",
                    f"- Actuals source: {actual.source_name} ({actual.source_date.isoformat()})",
                    f"- Actuals note: {actual.notes or 'None'}",
                ]
            )
        lines.extend(
            [
                "",
                "### Outcome Comparison",
                "",
                "| Metric | Consensus | Actual | Delta | Delta % | Band |",
                "| --- | ---: | ---: | ---: | ---: | --- |",
                _metric_row("EPS", item.eps),
                _metric_row("Revenue", item.revenue),
                "",
                "### Move Comparison",
                "",
                "| Implied move | Actual move | Delta | Matched scenario |",
                "| ---: | ---: | ---: | --- |",
                (
                    f"| {item.move.implied_move_percent:.2f}% | {_fmt_percent(item.move.actual_move_percent)} | "
                    f"{_fmt_percent(item.move.delta_percent)} | {item.move.matched_scenario} |"
                ),
                "",
                "### Thesis Ledger Handoff",
                "",
            ]
        )
        lines.extend(f"- {note}" for note in item.thesis_ledger_handoff)
        lines.extend(["", "### Review Queue", ""])
        lines.extend(f"- {entry}" for entry in item.review_queue)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html_index(playbooks: Iterable[EventPlaybook]) -> str:
    items = list(playbooks)
    cards = []
    for item in items:
        event = item.event
        review_items = "".join(f"<li>{html.escape(entry)}</li>" for entry in item.review_queue)
        risk_questions = "".join(f"<li>{html.escape(question)}</li>" for question in item.risk_questions)
        if not risk_questions:
            risk_questions = "<li>None provided.</li>"
        cards.append(
            "<section class=\"card\">"
            f"<h2>{html.escape(event.ticker)} - {html.escape(event.company)}</h2>"
            f"<p><strong>Event:</strong> {event.date.isoformat()} | "
            f"<strong>Period:</strong> {html.escape(event.fiscal_period)} | "
            f"<strong>Freshness:</strong> {html.escape(item.freshness)}</p>"
            f"<p><strong>Attention:</strong> {item.attention_score}/100 | "
            f"<strong>Implied move:</strong> {event.implied_move_percent:.2f}%</p>"
            "<table><thead><tr><th>Scenario</th><th>Price move</th><th>Exposure delta</th></tr></thead><tbody>"
            + "".join(
                f"<tr><td>{html.escape(band.name)}</td><td>{band.price_move_percent:.2f}%</td><td>{band.exposure_delta:.2f}</td></tr>"
                for band in item.scenario_bands
            )
            + "</tbody></table>"
            "<div class=\"grid\">"
            "<div><h3>Risk questions</h3><ul>" + risk_questions + "</ul></div>"
            "<div><h3>Review queue</h3><ul>" + review_items + "</ul></div>"
            "</div>"
            "</section>"
        )
    total_review_items = sum(len(item.review_queue) for item in items)
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Earnings Event Playbook Demo</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; color: #1f2933; background: #f7f8fa; }
    header { background: #12343b; color: white; padding: 32px max(24px, 8vw); }
    main { max-width: 1040px; margin: 0 auto; padding: 24px; }
    .notice { border-left: 4px solid #d9822b; background: #fff8f0; padding: 12px 16px; }
    .card { background: white; border: 1px solid #d9e2ec; border-radius: 8px; padding: 18px; margin: 18px 0; }
    .summary { display: flex; flex-wrap: wrap; gap: 12px; margin: 18px 0; }
    .summary div { background: white; border: 1px solid #d9e2ec; padding: 12px 14px; min-width: 150px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin-top: 16px; }
    table { border-collapse: collapse; width: 100%; margin-top: 12px; }
    th, td { border-bottom: 1px solid #e4e7eb; padding: 8px; text-align: left; }
    th { background: #f0f4f8; }
    h3 { margin-bottom: 8px; }
    ul { margin-top: 0; padding-left: 20px; }
  </style>
</head>
<body>
  <header>
    <h1>Earnings Event Playbook Demo</h1>
    <p>Static local-fixture preview. No JavaScript, live data, broker connection, orders, or advice.</p>
  </header>
  <main>
    <p class="notice">Use this page as a review artifact only. Verify any fixture data against source materials before making decisions.</p>
    <section class="summary" aria-label="Demo summary">
      <div><strong>Events</strong><br>""" + str(len(items)) + """</div>
      <div><strong>Review items</strong><br>""" + str(total_review_items) + """</div>
      <div><strong>Runtime deps</strong><br>0</div>
      <div><strong>Data mode</strong><br>local fixtures</div>
    </section>
    """ + "\n    ".join(cards) + """
  </main>
</body>
</html>
"""


def _fmt_number(value: float | None) -> str:
    if value is None:
        return "not provided"
    return f"{value:.2f}"


def _fmt_percent(value: float | None) -> str:
    if value is None:
        return "not provided"
    return f"{value:.2f}%"


def _metric_row(label: str, comparison) -> str:
    return (
        f"| {label} | {_fmt_number(comparison.consensus)} | {_fmt_number(comparison.actual)} | "
        f"{_fmt_number(comparison.delta)} | {_fmt_percent(comparison.delta_percent)} | {comparison.band} |"
    )
