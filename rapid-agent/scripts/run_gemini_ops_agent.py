#!/usr/bin/env python3
"""Run the local Gemini Operations Navigator demo."""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_DIR = ROOT / "case_data"
REPORT_DIR = ROOT / "reports"
PROTOTYPE_DIR = ROOT / "prototype"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_run() -> dict:
    ticket = load_json(CASE_DIR / "support_ticket.json")
    tools = load_json(CASE_DIR / "tool_catalog.json")["tools"]
    policy = (CASE_DIR / "refund_policy.md").read_text(encoding="utf-8")

    tool_trace = [
        {
            "step": 1,
            "tool": "policy_mcp.retrieve_refund_policy",
            "status": "success",
            "evidence_id": "kb-refund-2026-05",
            "cost_usd_estimate": 0.001,
        },
        {
            "step": 2,
            "tool": "billing_mcp.check_recent_usage",
            "status": "success",
            "evidence_id": "usage-sup-1042",
            "cost_usd_estimate": 0.002,
            "result": "No new seats used after renewal in packaged case.",
        },
        {
            "step": 3,
            "tool": "gemini.generate_grounded_draft",
            "status": "success",
            "evidence_id": "draft-sup-1042",
            "cost_usd_estimate": 0.018,
            "result": "Draft cites refund policy and avoids promising approval.",
        },
        {
            "step": 4,
            "tool": "gmail_mcp.send_customer_reply",
            "status": "blocked_pending_human_approval",
            "evidence_id": "approval-gate-sup-1042",
            "cost_usd_estimate": 0,
            "result": "High-risk customer-facing action blocked until manager approval.",
        },
    ]
    total_cost = round(sum(float(row["cost_usd_estimate"]) for row in tool_trace), 3)
    budget = 0.05

    draft = (
        "I found the renewal-refund policy. Because the renewal was yesterday and "
        "the packaged usage check shows no new seats were used, this may qualify "
        "for manager review. I cannot promise the refund yet; a support manager "
        "must approve the exception first. Evidence: kb-refund-2026-05, usage-sup-1042."
    )
    run = {
        "case_id": ticket["case_id"],
        "ticket_id": ticket["ticket_id"],
        "model_route": "Gemini/Vertex-ready local demo",
        "partner_pattern": "MCP-style policy, billing, ticket, and action tools with Arize/OpenInference-compatible trace export",
        "partner_track": "Arize",
        "observability_route": "OpenInference-compatible JSONL trace for tool calls, cost, evidence, and approval boundary",
        "budget_usd": budget,
        "projected_cost_usd": total_cost,
        "cost_within_budget": total_cost <= budget,
        "tools": tools,
        "tool_trace": tool_trace,
        "grounded_draft": draft,
        "policy_excerpt": policy,
        "human_approval_required": True,
        "blocked_action": "gmail_mcp.send_customer_reply",
        "claim_boundary": "verified_local_mcp_workflow_no_live_google_deployment_claim",
    }
    return run


def openinference_spans(run: dict) -> list[dict]:
    spans: list[dict] = []
    for row in run["tool_trace"]:
        step = int(row["step"])
        spans.append(
            {
                "trace_id": f"{run['case_id']}-trace",
                "span_id": f"{run['case_id']}-span-{step:02d}",
                "parent_span_id": None,
                "name": row["tool"],
                "span_kind": "TOOL",
                "start_time": f"2026-05-20T00:00:{step * 5:02d}Z",
                "end_time": f"2026-05-20T00:00:{step * 5 + 2:02d}Z",
                "status": row["status"],
                "attributes": {
                    "openinference.span.kind": "TOOL",
                    "input.value": run["ticket_id"],
                    "output.value": row.get("result", row["status"]),
                    "tool.name": row["tool"],
                    "tool.step": step,
                    "evidence.id": row["evidence_id"],
                    "cost.usd.estimate": row["cost_usd_estimate"],
                    "approval.required": row["status"] == "blocked_pending_human_approval",
                    "human_approval_required": run["human_approval_required"],
                    "projected_cost_usd": run["projected_cost_usd"],
                },
            }
        )
    return spans


def terminal_lines(run: dict) -> list[str]:
    lines = [
        "$ python3 rapid-agent/scripts/run_gemini_ops_agent.py --case CASE-CLOUD-003",
        f"[case] {run['case_id']} / {run['ticket_id']}",
        "[mode] Gemini Operations Navigator: MCP tools + cost guardrails + human approval",
        f"[budget] max=${run['budget_usd']:.2f}",
        "",
    ]
    for row in run["tool_trace"]:
        lines.append(f"[tool] {row['tool']}: {row['status']}")
        lines.append(f"       evidence: {row['evidence_id']} cost=${float(row['cost_usd_estimate']):.3f}")
        if row.get("result"):
            lines.append(f"       result: {row['result']}")
    lines.extend(
        [
            "",
            f"[cost] projected=${run['projected_cost_usd']:.3f} within_budget={run['cost_within_budget']}",
            "[approval] customer-facing send is blocked until support manager approval",
            "[boundary] verified local MCP workflow; no live Google Cloud deployment claimed",
        ]
    )
    return lines


def write_terminal_html(lines: list[str]) -> None:
    escaped = "\n".join(html.escape(line) for line in lines)
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Terminal Session — Gemini Operations Navigator</title>
  <style>
    body {{ margin: 0; background: #0b1220; color: #dbeafe; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 28px 18px; }}
    .bar {{ background: #1f2937; color: #f8fafc; border: 1px solid #334155; border-radius: 8px 8px 0 0; padding: 10px 14px; font-family: Inter, system-ui, sans-serif; }}
    pre {{ margin: 0; background: #020617; border: 1px solid #334155; border-top: 0; border-radius: 0 0 8px 8px; padding: 18px; white-space: pre-wrap; line-height: 1.5; font-size: 14px; }}
  </style>
</head>
<body><main><div class="bar">CASE-CLOUD-003 · Gemini/MCP terminal run</div><pre>{escaped}</pre></main></body>
</html>
"""
    (PROTOTYPE_DIR / "terminal-session.html").write_text(content, encoding="utf-8")


def write_reports(run: dict, lines: list[str]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    PROTOTYPE_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "agent-run.json").write_text(json.dumps(run, indent=2) + "\n", encoding="utf-8")
    (REPORT_DIR / "mcp-tool-trace.jsonl").write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in run["tool_trace"]) + "\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "openinference-trace.jsonl").write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in openinference_spans(run)) + "\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "cost-ledger.json").write_text(
        json.dumps(
            {
                "case_id": run["case_id"],
                "budget_usd": run["budget_usd"],
                "projected_cost_usd": run["projected_cost_usd"],
                "cost_within_budget": run["cost_within_budget"],
                "stop_rule": "Block additional model/tool loops when projected_cost_usd exceeds budget_usd.",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "approval-checkpoint.md").write_text(
        "# Approval Checkpoint\n\n"
        "- Blocked action: `gmail_mcp.send_customer_reply`\n"
        "- Reason: customer-facing financial answer\n"
        "- Required approver: support manager\n"
        "- Evidence before approval: `kb-refund-2026-05`, `usage-sup-1042`, `draft-sup-1042`\n",
        encoding="utf-8",
    )
    (REPORT_DIR / "terminal-transcript.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_terminal_html(lines)


def main() -> None:
    run = build_run()
    lines = terminal_lines(run)
    write_reports(run, lines)
    print("\n".join(lines))


if __name__ == "__main__":
    main()
