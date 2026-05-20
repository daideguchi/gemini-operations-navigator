# Submission Package — Gemini Operations Navigator

## Project Title

Gemini Operations Navigator

## Short Description

Gemini + MCP for support operations with visible cost guardrails, evidence-backed actions, and human approval checkpoints.

## Public Links

- Repository: https://github.com/daideguchi/gemini-operations-navigator
- Live demo: https://daideguchi.github.io/gemini-operations-navigator/
- Architecture: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/ARCHITECTURE.md

## Demo Video

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

Gemini Operations Navigator turns a customer support question into a controlled workflow: retrieve policy through MCP-style tools, check usage, draft a grounded answer, show projected cost, and stop before sending anything to the customer until a human manager approves it.

## What It Does

- Parses a packaged support ticket.
- Runs MCP-style policy, billing, ticket, and action tools.
- Drafts a grounded reply with evidence IDs.
- Records projected tool/model cost.
- Blocks the customer-facing send until human approval.
- Publishes a workflow UI, terminal transcript, cost ledger, and tool trace.

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- MCP-style tool model
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
video_seconds=72.8
claim_boundary=verified_local_mcp_workflow_no_live_google_deployment_claim
```

## Verification Commands

```bash
cd /path/to/gemini-operations-navigator
bash rapid-agent/scripts/run_google_local_checks.sh
```

## Screenshots

- `architecture-diagram.svg`
- `rapid-agent/media/gemini-operations-navigator-full.png`
- `rapid-agent/media/gemini-terminal-session-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## What Makes It Different

This is not just "Gemini answers a question." It is an operations workflow where action, cost, evidence, and approval are visible before the agent takes a risky step.

## Claim Boundary

This is a local verified workflow prototype. It does not claim live Google Cloud deployment, final promotional-credit accounting, or unsupervised customer-facing action.
