#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

cd "$REPO_ROOT/shared-agentops-engine"
python3 scripts/generate_portfolio_artifacts.py >/tmp/google-shared-generate.log
python3 scripts/verify_artifacts.py >/tmp/google-shared-verify.log

cd "$REPO_ROOT"
python3 rapid-agent/scripts/run_vertex_gemini_live.py >/tmp/google-vertex-live.log
node rapid-agent/scripts/run_phoenix_mcp_probe.mjs >/tmp/google-phoenix-mcp.log
python3 rapid-agent/scripts/run_gemini_ops_agent.py >/tmp/google-terminal.log
python3 rapid-agent/scripts/build_gemini_workflow_demo.py >/tmp/google-workflow.log
bash rapid-agent/scripts/build_demo_video.sh >/tmp/google-video.log

python3 - <<'PY'
import json
import subprocess
from pathlib import Path

root = Path("rapid-agent")
required = [
    root / "reports" / "agent-run.json",
    root / "reports" / "mcp-tool-trace.jsonl",
    root / "reports" / "openinference-trace.jsonl",
    root / "reports" / "cost-ledger.json",
    root / "reports" / "approval-checkpoint.md",
    root / "reports" / "terminal-transcript.txt",
    root / "reports" / "vertex-gemini-live-proof.json",
    root / "reports" / "phoenix-mcp-runtime-proof.json",
    root / "agent-builder" / "agent-builder-runtime-manifest.json",
    root / "prototype" / "terminal-session.html",
    root / "prototype" / "gemini-operations-navigator.html",
    root / "media" / "gemini-operations-navigator-demo.mp4",
]
missing = [str(path) for path in required if not path.exists() or path.stat().st_size == 0]
if missing:
    raise SystemExit(f"missing outputs: {missing}")

run = json.loads((root / "reports" / "agent-run.json").read_text())
if not run["cost_within_budget"]:
    raise SystemExit("cost guardrail failed")
if not run["human_approval_required"]:
    raise SystemExit("approval gate missing")
if run["tool_trace"][-1]["status"] != "blocked_pending_human_approval":
    raise SystemExit("customer-facing send was not blocked")
if run.get("partner_track") != "Arize":
    raise SystemExit("Arize partner track marker missing")
if run.get("target_user") != "support operations manager":
    raise SystemExit("target user missing")
if "AI support work" not in run.get("problem_solved", ""):
    raise SystemExit("problem solved statement missing")
if "Gemini" not in run.get("ai_usage", ""):
    raise SystemExit("AI usage statement missing")

vertex = json.loads((root / "reports" / "vertex-gemini-live-proof.json").read_text())
allowed_vertex_statuses = {
    "ok",
    "blocked_by_google_cloud_account_state",
    "blocked_by_billing_state",
    "blocked_by_quota_state",
}
if vertex.get("status") not in allowed_vertex_statuses:
    raise SystemExit(f"unexpected Vertex proof status: {vertex.get('status')}")
if vertex.get("status") != "ok":
    attempts = vertex.get("attempts", [])
    if not attempts:
        raise SystemExit("Vertex block report missing attempts")
    if not any(row.get("error_message") for row in attempts):
        raise SystemExit("Vertex block report missing sanitized error message")

phoenix = json.loads((root / "reports" / "phoenix-mcp-runtime-proof.json").read_text())
if phoenix.get("status") != "ok":
    raise SystemExit("Phoenix MCP runtime proof failed")
if phoenix.get("tool_count", 0) < 4:
    raise SystemExit("Phoenix MCP tool list too small")
for tool_name in ["list-projects", "list-traces", "get-spans", "phoenix-support"]:
    if tool_name not in phoenix.get("selected_tools", []):
        raise SystemExit(f"Phoenix MCP selected tool missing: {tool_name}")

spans = [
    json.loads(line)
    for line in (root / "reports" / "openinference-trace.jsonl").read_text().splitlines()
    if line.strip()
]
if len(spans) != len(run["tool_trace"]):
    raise SystemExit("OpenInference span count does not match tool trace")
for span in spans:
    attrs = span.get("attributes", {})
    if attrs.get("openinference.span.kind") != "TOOL":
        raise SystemExit("OpenInference span kind missing")
    if not attrs.get("evidence.id"):
        raise SystemExit("OpenInference span missing evidence id")
    if "cost.usd.estimate" not in attrs:
        raise SystemExit("OpenInference span missing cost estimate")

transcript = (root / "reports" / "terminal-transcript.txt").read_text()
for needle in [
    "projected=$0.021",
    "blocked until support manager approval",
    "[vertex] status=",
    "[phoenix] status=ok",
    "[agent-builder] manifest=present",
]:
    if needle not in transcript:
        raise SystemExit(f"transcript missing: {needle}")

duration = float(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=nw=1:nk=1", str(root / "media" / "gemini-operations-navigator-demo.mp4")
], text=True).strip())
if duration < 45:
    raise SystemExit(f"demo video too short: {duration}")
audio = subprocess.check_output([
    "ffprobe", "-v", "error", "-select_streams", "a",
    "-show_entries", "stream=codec_type", "-of", "csv=p=0",
    str(root / "media" / "gemini-operations-navigator-demo.mp4")
], text=True).strip()
if "audio" not in audio:
    raise SystemExit("demo video missing audio")

print("google_local_checks_ok")
print(f"mcp_tool_calls={len(run['tool_trace'])}")
print(f"projected_cost_usd={run['projected_cost_usd']}")
print(f"cost_within_budget={run['cost_within_budget']}")
print("human_approval_required=true")
print(f"openinference_spans={len(spans)}")
print("partner_track=Arize")
print(f"vertex_status={vertex['status']}")
print(f"phoenix_mcp_tool_count={phoenix['tool_count']}")
print("agent_builder_manifest=present")
print(f"video_seconds={duration:.1f}")
print(f"claim_boundary={run['claim_boundary']}")
PY
