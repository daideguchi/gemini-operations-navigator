# Devpost Draft — Gemini Operations Navigator

## Tagline

Gemini + MCP for support operations with visible cost guardrails, evidence-backed actions, and human approval checkpoints.

## What It Does

Gemini Operations Navigator runs a local support-operations workflow.

A customer asks for a renewal refund. The agent retrieves the refund policy through an MCP-style policy tool, checks usage through a billing tool, drafts a grounded response, records projected cost, and blocks the customer-facing send until a manager approves it.

Outputs:

- terminal transcript
- MCP tool trace
- cost ledger
- approval checkpoint
- workflow UI
- architecture diagram
- demo video

## Why It Matters

AI agents become risky when tool calls, spend, evidence, and customer-facing actions are hidden.

This project treats cost and approval as product features. The agent can help, but it must show what it used, how much it costs, and where a human needs to decide.

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- MCP-style tool model
- ImageMagick
- ffmpeg
- Edge TTS neural narration

## Verification Output

```text
google_local_checks_ok
mcp_tool_calls=4
projected_cost_usd=0.021
cost_within_budget=True
human_approval_required=true
video_seconds=72.8
claim_boundary=verified_local_mcp_workflow_no_live_google_deployment_claim
```

## Claim Boundary

This is a verified local workflow prototype. It does not claim live Google Cloud deployment, final promotional-credit accounting, or unsupervised customer-facing action.
