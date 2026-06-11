# Submission Package — Gemini Operations Navigator

## Project Title

Gemini Operations Navigator

## Short Description

Gemini + MCP for support operations managers who need evidence-backed AI drafts, visible cost guardrails, and human approval before customer-facing action.

## Public Links

- Repository: https://github.com/daideguchi/gemini-operations-navigator
- Live demo: https://daideguchi.github.io/gemini-operations-navigator/
- YouTube demo: https://www.youtube.com/watch?v=kt34TmPsT4g
- Architecture: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/ARCHITECTURE.md
- Arize/OpenInference trace: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/openinference-trace.jsonl
- Phoenix MCP runtime proof: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/phoenix-mcp-runtime-proof.json
- Vertex rerun status: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/vertex-gemini-live-proof.json
- Agent Builder manifest: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/agent-builder/agent-builder-runtime-manifest.json

## Demo Video

YouTube demo:

- https://www.youtube.com/watch?v=kt34TmPsT4g

Final local demo video:

- `rapid-agent/media/gemini-operations-navigator-demo.mp4`

Compatibility copy:

- `rapid-agent/media/gemini-operations-navigator-demo-draft.mp4`

Regenerate:

```bash
bash rapid-agent/scripts/build_demo_video.sh
```

## The Simple Story

Gemini agents should not be mysterious operators. They should be visible coworkers.

Gemini Operations Navigator turns a customer support refund question into a controlled workflow for a support operations manager: retrieve policy through MCP-style tools, check usage, draft a grounded answer with Gemini, show projected cost, expose trace tooling through Phoenix MCP, and stop before sending anything to the customer until a human manager approves it.

## What It Does

- Parses a packaged support ticket.
- Runs MCP-style policy, billing, ticket, and action tools.
- Drafts a grounded reply with evidence IDs.
- Records projected tool/model cost.
- Exports an Arize/OpenInference-compatible trace for every tool step.
- Captures an actual Arize Phoenix MCP server handshake and tool list.
- Ships an Agent Builder-ready runtime manifest for model, MCP, tools, budget, and approval policy.
- Records the current Vertex AI Gemini rerun status without hiding Google Cloud account stoplines.
- Blocks the customer-facing send until human approval.
- Publishes a workflow UI, terminal transcript, cost ledger, and tool trace.

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- MCP-style tool model
- Arize/OpenInference-compatible trace export
- Gemini / Google Cloud / ADK-ready architecture
- Google Cloud Agent Builder-ready runtime manifest
- Arize Phoenix MCP runtime proof
- ImageMagick
- ffmpeg
- Edge TTS neural narration

## What Is Working

```text
google_local_checks_ok
mcp_tool_calls=4
projected_cost_usd=0.021
cost_within_budget=True
human_approval_required=true
openinference_spans=4
partner_track=Arize
video_seconds=72.8
vertex_status=blocked_by_google_cloud_account_state
phoenix_mcp_tool_count=27
agent_builder_manifest=present
claim_boundary=local_workflow_verified_phoenix_mcp_verified_vertex_rerun_blocked_if_google_consumer_suspended_no_customer_send_claim
```

## Verification Commands

```bash
cd /path/to/gemini-operations-navigator
bash rapid-agent/scripts/run_google_local_checks.sh
```

## Screenshots

- `architecture-diagram.svg`
- `rapid-agent/reports/openinference-trace.jsonl`
- `rapid-agent/reports/phoenix-mcp-runtime-proof.json`
- `rapid-agent/reports/vertex-gemini-live-proof.json`
- `rapid-agent/agent-builder/agent-builder-runtime-manifest.json`
- `rapid-agent/media/gemini-operations-navigator-full.png`
- `rapid-agent/media/gemini-terminal-session-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## What Makes It Different

This is not just "Gemini answers a question." It is an operations workflow where action, cost, evidence, and approval are visible before the agent takes a risky step.

## Claim Boundary

This is a verified local workflow prototype with Phoenix MCP runtime proof and an Agent Builder-ready manifest. It records the current Vertex rerun status and does not claim production Google Cloud deployment, final promotional-credit accounting, or unsupervised customer-facing action.

## Devpost Field Copy

- `rapid-agent/submission/devpost-submit-manual.md`
