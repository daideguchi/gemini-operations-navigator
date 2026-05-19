# Gemini Operations Navigator

Gemini Operations Navigator is a cost-aware, approval-first agent workflow for the Google Cloud Rapid Agent Hackathon.

The product idea is not "let the AI do everything." It is: give Gemini action tools, MCP context, cost limits, and human checkpoints so operational work can move faster without becoming opaque.

Submission package: [SUBMISSION_PACKAGE.md](SUBMISSION_PACKAGE.md)

## Demo

![Gemini Operations Navigator demo](rapid-agent/media/gemini-operations-navigator-full.png)

Open locally:

- `rapid-agent/prototype/gemini-operations-navigator.html`
- `shared-agentops-engine/web/index.html`

## What It Shows

- MCP-style tool plan
- Agent event timeline
- Cost guardrail policy
- Human approval checkpoint
- Evidence-backed handoff summary

## Run Locally

```bash
cd shared-agentops-engine
python3 scripts/generate_portfolio_artifacts.py
python3 scripts/verify_artifacts.py
```

```bash
cd ../rapid-agent
python3 scripts/build_gemini_workflow_demo.py
```

Expected proof:

```text
verify_ok
status: ok
```

## Hackathon Boundary

Safe claim:

- A local Gemini/MCP workflow prototype, cost policy, and approval model are generated.

Not claimed yet:

- Live Google Cloud deployment.
- New paid-looking API usage.
- Final billing or credit behavior.

## Project Layout

- `rapid-agent/` - Google-focused prototype, screenshot, cost guardrail, and Devpost draft
- `shared-agentops-engine/` - shared event stream, adapters, dashboard, and verifier
