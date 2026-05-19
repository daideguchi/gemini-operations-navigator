# Submission Package — Gemini Operations Navigator

## Project Title

Gemini Operations Navigator

## Short Description

Gemini + MCP for support operations with visible cost guardrails, evidence-backed actions, and human approval checkpoints.

## Repository

https://github.com/daideguchi/gemini-operations-navigator

## Try It Out

Open these local demo files after cloning the repository:

- `rapid-agent/prototype/gemini-operations-navigator.html`
- `shared-agentops-engine/web/index.html`

## Screenshots

- `rapid-agent/media/gemini-operations-navigator-full.png`
- `shared-agentops-engine/media/shared-dashboard-full.png`

## Inspiration

Gemini agents are useful when they can act with tools, but action without cost limits, evidence, and approval points is risky.

This project treats cost control and human approval as product features, not hidden backend concerns.

## What It Does

Gemini Operations Navigator shows an operations workflow where an agent:

- creates a support workflow plan
- retrieves policy through an MCP-style tool
- drafts a grounded response
- logs cost signals
- pauses for human approval
- records the final handoff

## How We Built It

- Shared AgentOps event stream
- Gemini/MCP workflow specification
- Cost guardrail policy JSON
- Local HTML workflow demo
- Human approval checkpoint model

## Built With

- Python
- HTML/CSS
- JSON / JSONL
- Gemini workflow model
- MCP-style tool plan

## What Is Working

```text
verify_ok
status: ok
event_count=7
mcp_tools=3
human_control_points=1
```

## Verification Commands

```bash
cd shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

```bash
cd ../rapid-agent
python3 scripts/build_gemini_workflow_demo.py
```

## Demo Script Summary

1. Show the support-operations workflow.
2. Show MCP-style policy retrieval.
3. Show the grounded draft and cost signal.
4. Show the human approval checkpoint.
5. Explain how the workflow keeps agent action transparent.

## What Makes It Different

This is not just "Gemini answers a question." It is an operations workflow where action, cost, evidence, and approval are visible.

## Challenges

The main challenge was respecting the cost route. The demo currently stays local and explicit about its boundary instead of triggering unverified paid-looking API use.

## Accomplishments

- Built a Gemini/MCP workflow demo
- Added a cost guardrail policy
- Added human approval control points
- Published a clean public repository

## What We Learned

Agent workflows become more trustworthy when cost and approval are visible to the operator.

## What's Next

Verify the current Google Cloud / Vertex / Gemini route for this project and connect the workflow to a live agent path only after cost behavior is confirmed.

## Claim Boundary

This is a local verified workflow prototype.

It does not claim live Google Cloud deployment or fresh live Gemini calls in this repository yet.
