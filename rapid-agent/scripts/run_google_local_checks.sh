#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"

cd "$REPO_ROOT/shared-agentops-engine"
python3 scripts/generate_portfolio_artifacts.py >/tmp/google-shared-generate.log
python3 scripts/verify_artifacts.py >/tmp/google-shared-verify.log

cd "$REPO_ROOT"
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
    root / "reports" / "cost-ledger.json",
    root / "reports" / "approval-checkpoint.md",
    root / "reports" / "terminal-transcript.txt",
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

transcript = (root / "reports" / "terminal-transcript.txt").read_text()
for needle in ["projected=$0.021", "blocked until support manager approval", "no live Google Cloud deployment claimed"]:
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
print(f"video_seconds={duration:.1f}")
print("claim_boundary=verified_local_mcp_workflow_no_live_google_deployment_claim")
PY
