# Gemini Operations Navigator

Gemini + MCP for support operations with visible cost guardrails, evidence-backed actions, and human approval checkpoints.

Live demo: https://daideguchi.github.io/gemini-operations-navigator/

Submission package: [SUBMISSION_PACKAGE.md](SUBMISSION_PACKAGE.md)

Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)

## Judge Quick Read

**Who is this for?** Support operations teams that want AI agents to help with customer-facing work.

**What problem does it solve?** Gemini can retrieve, draft, and act, but a support agent becomes risky when tool calls, spend, evidence, and customer-facing actions are hidden.

**How does it solve it?** The workflow runs MCP-style policy, billing, and ticket tools, creates a grounded draft, records projected cost, and blocks the customer reply until a human manager approves it.

**What is verified?** A local terminal run, MCP tool trace, cost ledger, approval checkpoint, workflow UI, architecture diagram, narrated demo video, and public GitHub Pages review hub.

## Demo

![Architecture diagram](architecture-diagram.svg)

![Gemini Operations Navigator demo](rapid-agent/media/gemini-operations-navigator-full.png)

![Terminal proof](rapid-agent/media/gemini-terminal-session-full.png)

Demo video:

```text
rapid-agent/media/gemini-operations-navigator-demo.mp4
```

Open in browser:

- https://daideguchi.github.io/gemini-operations-navigator/
- https://daideguchi.github.io/gemini-operations-navigator/rapid-agent/prototype/gemini-operations-navigator.html
- https://daideguchi.github.io/gemini-operations-navigator/rapid-agent/prototype/terminal-session.html

## Run Locally

```bash
cd /path/to/gemini-operations-navigator
bash rapid-agent/scripts/run_google_local_checks.sh
```

Expected proof:

```text
google_local_checks_ok
mcp_tool_calls=4
projected_cost_usd=0.021
cost_within_budget=True
human_approval_required=true
claim_boundary=verified_local_mcp_workflow_no_live_google_deployment_claim
```

## What It Shows

- MCP-style tool calls for policy, usage, draft, and customer reply.
- A grounded reply that cites evidence instead of promising a refund.
- A cost ledger that keeps projected spend visible.
- A high-risk customer-facing send blocked until manager approval.
- A submission boundary that avoids claiming live Google Cloud deployment before verification.

## Key Files

- `rapid-agent/case_data/` - support ticket, policy excerpt, and tool catalog.
- `rapid-agent/scripts/run_gemini_ops_agent.py` - terminal workflow.
- `rapid-agent/reports/mcp-tool-trace.jsonl` - replayable tool trace.
- `rapid-agent/reports/cost-ledger.json` - budget and projected cost.
- `rapid-agent/reports/approval-checkpoint.md` - human approval packet.
- `rapid-agent/prototype/terminal-session.html` - terminal proof page.
- `ARCHITECTURE.md` - component and data-flow explanation.

## Claim Boundary

Safe claim:

- A local Gemini/MCP workflow prototype runs against packaged case data and produces tool trace, cost ledger, approval checkpoint, workflow UI, and natural English demo video.

Not claimed yet:

- Live Google Cloud deployment.
- Final promotional-credit accounting.
- Unsupervised customer-facing action.
