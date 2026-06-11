#!/usr/bin/env python3
"""Build the Google Cloud Rapid Agent local demo artifact."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = ROOT.parent / "shared-agentops-engine"
WORKFLOW_FILE = SHARED_ROOT / "adapters" / "google" / "gemini_mcp_workflow.json"
OUT_FILE = ROOT / "prototype" / "gemini-operations-navigator.html"
POLICY_FILE = ROOT / "reports" / "cost-guardrail-policy.json"
OPENINFERENCE_FILE = ROOT / "reports" / "openinference-trace.jsonl"
VERTEX_PROOF_FILE = ROOT / "reports" / "vertex-gemini-live-proof.json"
PHOENIX_PROOF_FILE = ROOT / "reports" / "phoenix-mcp-runtime-proof.json"
AGENT_BUILDER_MANIFEST = ROOT / "agent-builder" / "agent-builder-runtime-manifest.json"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def risk_class(risk: str) -> str:
    if risk in {"critical", "high"}:
        return "danger"
    if risk == "medium":
        return "warn"
    if risk == "low":
        return "ok"
    return "quiet"


def build_tool_cards(workflow: dict[str, Any]) -> str:
    rows: list[str] = []
    for tool in workflow["mcp_tools"]:
        evidence = ", ".join(tool["evidence"]) if tool["evidence"] else "planned"
        rows.append(
            f"""
            <article class="tool-card">
              <span class="tool-name">{esc(tool["name"])}</span>
              <p>{esc(tool["purpose"])}</p>
              <span class="evidence">{esc(evidence)}</span>
            </article>
            """
        )
    return "\n".join(rows)


def build_event_rows(events: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for event in events:
        rows.append(
            f"""
            <article class="event-row">
              <div>
                <span class="event-id">{esc(event["event_id"])}</span>
                <span class="subtle">{esc(event["phase"])}</span>
              </div>
              <div class="event-main">
                <strong>{esc(event["event_type"])}</strong>
                <span>{esc(event["actor_type"])} / {esc(event["actor_name"])}</span>
                <p>{esc(event["summary"])}</p>
              </div>
              <span class="risk-pill {risk_class(event["risk_level"])}">{esc(event["risk_level"])}</span>
            </article>
            """
        )
    return "\n".join(rows)


def build_cost_rows(events: list[dict[str, Any]]) -> str:
    cost_events = [event for event in events if event.get("cost_usd_estimate") is not None]
    return "\n".join(
        f"""
        <tr>
          <td><span class="event-id">{esc(event["event_id"])}</span></td>
          <td>{esc(event["actor_name"])}</td>
          <td>${float(event.get("cost_usd_estimate", 0)):.3f}</td>
          <td>{esc(event.get("risk_reason", event["summary"]))}</td>
        </tr>
        """
        for event in cost_events
    )


def load_openinference_spans() -> list[dict[str, Any]]:
    if not OPENINFERENCE_FILE.exists():
        return []
    return [
        json.loads(line)
        for line in OPENINFERENCE_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_json_or_status(path: Path, status: str) -> dict[str, Any]:
    if not path.exists():
        return {"status": status}
    return json.loads(path.read_text(encoding="utf-8"))


def status_class(status: str) -> str:
    if status == "ok" or status == "present":
        return "ok"
    if status.startswith("blocked"):
        return "warn"
    return "danger"


def build_runtime_proof_cards() -> str:
    vertex = load_json_or_status(VERTEX_PROOF_FILE, "missing")
    phoenix = load_json_or_status(PHOENIX_PROOF_FILE, "missing")
    manifest_status = "present" if AGENT_BUILDER_MANIFEST.exists() else "missing"
    vertex_detail = vertex.get("model") or vertex.get("status")
    if vertex.get("status", "").startswith("blocked"):
        attempts = vertex.get("attempts", [])
        vertex_detail = attempts[0].get("error_message", vertex.get("status")) if attempts else vertex.get("status")

    cards = [
        {
            "title": "Vertex Gemini",
            "status": vertex.get("status", "missing"),
            "detail": vertex_detail,
            "link": "../reports/vertex-gemini-live-proof.json",
        },
        {
            "title": "Phoenix MCP",
            "status": phoenix.get("status", "missing"),
            "detail": f"{phoenix.get('tool_count', 0)} tools exposed by {phoenix.get('server_info', {}).get('name', 'server')}",
            "link": "../reports/phoenix-mcp-runtime-proof.json",
        },
        {
            "title": "Agent Builder",
            "status": manifest_status,
            "detail": "Deployment-ready manifest for model, MCP, tools, budget, and approval policy.",
            "link": "../agent-builder/agent-builder-runtime-manifest.json",
        },
    ]
    return "\n".join(
        f"""
        <article class="proof-card">
          <div>
            <strong>{esc(card["title"])}</strong>
            <span class="risk-pill {status_class(card["status"])}">{esc(card["status"])}</span>
          </div>
          <p>{esc(card["detail"])}</p>
          <a href="{esc(card["link"])}">Open proof</a>
        </article>
        """.strip()
        for card in cards
    )


def build_span_rows(spans: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"""
        <tr>
          <td>{esc(span["span_id"])}</td>
          <td>{esc(span["name"])}</td>
          <td>{esc(span["attributes"].get("evidence.id", ""))}</td>
          <td>${float(span["attributes"].get("cost.usd.estimate", 0)):.3f}</td>
        </tr>
        """
        for span in spans
    )


def build_html(workflow: dict[str, Any]) -> str:
    events = workflow["events"]
    spans = load_openinference_spans()
    total_cost = sum(float(event.get("cost_usd_estimate", 0) or 0) for event in events)
    approval_count = len(workflow["human_control_points"])
    mcp_count = len(workflow["mcp_tools"])
    risk_count = len(workflow["risk_events"])
    tool_cards = build_tool_cards(workflow)
    event_rows = build_event_rows(events)
    cost_rows = build_cost_rows(events)
    span_rows = build_span_rows(spans)
    proof_cards = build_runtime_proof_cards()

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Gemini Operations Navigator — Google Rapid Agent Demo</title>
  <style>
    :root {{
      --bg: #f6f7fb;
      --surface: #fff;
      --ink: #1f2937;
      --muted: #667085;
      --line: #d8e0ea;
      --brand: #1a73e8;
      --brand-soft: #e8f0fe;
      --green: #0b8043;
      --green-soft: #e8f5ec;
      --yellow: #b06000;
      --yellow-soft: #fff4df;
      --red: #b42318;
      --red-soft: #ffebe9;
      --shadow: 0 16px 36px rgba(31, 41, 55, 0.08);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}

    main {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 28px 18px 48px;
    }}

    .locator {{
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 12px;
    }}

    .hero {{
      background: #ffffff;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 28px;
      box-shadow: var(--shadow);
      display: grid;
      grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
      gap: 24px;
      align-items: start;
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.12;
      letter-spacing: 0;
    }}

    h2 {{
      margin: 0 0 12px;
      font-size: 20px;
      letter-spacing: 0;
    }}

    h3 {{
      margin: 0 0 8px;
      font-size: 16px;
      letter-spacing: 0;
    }}

    p {{ margin: 0; }}

    .hero-copy {{
      margin-top: 14px;
      color: var(--muted);
      font-size: 16px;
      max-width: 760px;
    }}

    .guardrail {{
      background: var(--brand-soft);
      border: 1px solid #b8cdf8;
      border-radius: 8px;
      padding: 16px;
    }}

    .guardrail strong {{
      display: block;
      margin-bottom: 8px;
      color: #174ea6;
    }}

    .metrics {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
      margin-top: 22px;
    }}

    .metric,
    .section,
    .tool-card {{
      background: var(--surface);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: 0 8px 24px rgba(31, 41, 55, 0.04);
    }}

    .metric {{
      padding: 16px;
      min-height: 108px;
    }}

    .metric strong {{
      display: block;
      font-size: 28px;
      line-height: 1;
      margin-bottom: 8px;
    }}

    .metric span {{
      color: var(--muted);
      font-size: 13px;
    }}

    .section {{
      margin-top: 22px;
      padding: 20px;
    }}

    .tool-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .tool-card {{
      padding: 16px;
      min-height: 162px;
    }}

    .proof-grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}

    .proof-card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #fff;
      display: grid;
      gap: 10px;
      min-height: 150px;
    }}

    .proof-card div {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }}

    .proof-card a {{
      color: var(--brand);
      font-weight: 800;
      text-decoration: none;
    }}

    .tool-name,
    .event-id {{
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      color: var(--brand);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }}

    .evidence {{
      display: inline-flex;
      margin-top: 12px;
      background: var(--green-soft);
      color: var(--green);
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 12px;
      font-weight: 800;
    }}

    .risk-pill {{
      display: inline-flex;
      align-items: center;
      width: fit-content;
      min-height: 24px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .risk-pill.warn {{ color: var(--yellow); background: var(--yellow-soft); }}
    .risk-pill.ok {{ color: var(--green); background: var(--green-soft); }}
    .risk-pill.quiet {{ color: var(--muted); background: #edf1f4; }}
    .risk-pill.danger {{ color: var(--red); background: var(--red-soft); }}

    .event-list {{
      display: grid;
      gap: 10px;
    }}

    .event-row {{
      display: grid;
      grid-template-columns: 180px minmax(0, 1fr) 92px;
      gap: 14px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #fff;
    }}

    .event-main {{
      display: grid;
      gap: 4px;
    }}

    .event-main span,
    .event-main p,
    .subtle {{
      color: var(--muted);
      font-size: 13px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}

    th {{
      text-align: left;
      color: var(--muted);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      border-bottom: 1px solid var(--line);
      padding: 10px 8px;
    }}

    td {{
      border-bottom: 1px solid var(--line);
      padding: 12px 8px;
      vertical-align: top;
    }}

    @media (max-width: 900px) {{
      .hero,
      .metrics,
      .proof-grid,
      .tool-grid {{
        grid-template-columns: 1fr;
      }}

      .event-row {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 620px) {{
      main {{ padding: 16px 12px 32px; }}
      h1 {{ font-size: 27px; }}
      table {{
        display: block;
        overflow-x: auto;
        white-space: nowrap;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <div class="locator">Google Cloud Rapid Agent · Gemini Operations Navigator · Demo Artifact</div>

    <section class="hero">
      <div>
        <h1>Use Gemini for support operations without losing cost control or human control.</h1>
        <p class="hero-copy">
          Built for support operations managers: Gemini drafts from policy evidence, MCP tools verify context,
          Phoenix MCP exposes observability tools, and a human approval gate blocks refund promises before customer send.
        </p>
      </div>
      <aside class="guardrail">
        <strong>Runtime boundary</strong>
        <p>Current Google Cloud rerun is recorded honestly. If the project is suspended, the proof says so and the workflow stays inside the no-out-of-pocket guardrail.</p>
      </aside>
    </section>

    <section class="metrics">
      <div class="metric"><strong>{len(events)}</strong><span>workflow events</span></div>
      <div class="metric"><strong>{mcp_count}</strong><span>MCP tools in the plan</span></div>
      <div class="metric"><strong>{len(spans)}</strong><span>Arize/OpenInference spans</span></div>
      <div class="metric"><strong>{risk_count}</strong><span>cost/risk guardrail event</span></div>
      <div class="metric"><strong>${total_cost:.2f}</strong><span>sample estimated spend</span></div>
    </section>

    <section class="section">
      <h2>Runtime Proof</h2>
      <p>These files are generated by <span class="event-id">run_google_local_checks.sh</span> so the submission claim matches the current runtime state.</p>
      <div class="proof-grid">{proof_cards}</div>
    </section>

    <section class="section">
      <h2>MCP Tool Plan</h2>
      <div class="tool-grid">{tool_cards}</div>
    </section>

    <section class="section">
      <h2>Cost Guardrail</h2>
      <table>
        <thead>
          <tr>
            <th>Event</th>
            <th>Actor</th>
            <th>Estimate</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>{cost_rows}</tbody>
      </table>
    </section>

    <section class="section">
      <h2>Arize / OpenInference Trace</h2>
      <p>Every tool step exports a span with the tool name, evidence ID, cost estimate, and approval boundary so judges can inspect the agent's operational behavior.</p>
      <table>
        <thead>
          <tr>
            <th>Span</th>
            <th>Tool</th>
            <th>Evidence</th>
            <th>Cost</th>
          </tr>
        </thead>
        <tbody>{span_rows}</tbody>
      </table>
    </section>

    <section class="section">
      <h2>Human Control</h2>
      <p>Human approval point: <span class="event-id">{esc(", ".join(workflow["human_control_points"]))}</span>. Expensive model calls are approved for escalation-only use.</p>
    </section>

    <section class="section">
      <h2>Workflow Timeline</h2>
      <div class="event-list">{event_rows}</div>
    </section>
  </main>
</body>
</html>
"""


def write_policy(workflow: dict[str, Any]) -> None:
    policy = {
        "product": workflow["name"],
        "case_id": workflow["case_id"],
        "billing_boundary": "local_demo_only_no_new_api_call_no_out_of_pocket_spend",
        "current_auth_cache_summary": "Vertex AI route was previously verified in ops/.ai_auth_cache.json, but the $100 Google Cloud Rapid Agent hackathon credit pool is exhausted and promotional-credit deduction must not be assumed.",
        "rules": [
            "Use low-cost model/tool path for routine retrieval and drafting.",
            "Reserve expensive model calls for human-approved escalations only.",
            "Stop or downgrade when projected monthly spend exceeds prototype budget.",
            "Never click Google AI Studio prepay, buy credits, auto-reload, or payment confirmation without DD approval.",
            "Do not assume a $100 Google Cloud hackathon credit code will arrive; use only free/no-out-of-pocket routes.",
        ],
        "evidence": workflow["risk_events"] + workflow["human_control_points"],
        "credit_update_2026_05_30": "Devpost said the hackathon-issued $100 Google Cloud credit code pool is exhausted; standard Google Cloud free trial remains a supported eligibility path.",
    }
    POLICY_FILE.parent.mkdir(parents=True, exist_ok=True)
    POLICY_FILE.write_text(json.dumps(policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    workflow = json.loads(WORKFLOW_FILE.read_text(encoding="utf-8"))
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_html(workflow), encoding="utf-8")
    write_policy(workflow)
    print(
        json.dumps(
            {
                "status": "ok",
                "source": str(WORKFLOW_FILE.relative_to(ROOT.parent)),
                "output": str(OUT_FILE.relative_to(ROOT)),
                "policy": str(POLICY_FILE.relative_to(ROOT)),
                "event_count": len(workflow["events"]),
                "mcp_tools": len(workflow["mcp_tools"]),
                "human_control_points": len(workflow["human_control_points"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
