# Gemini Operations Navigator

Target: Google Cloud Rapid Agent Hackathon

Status: P2 submission-ready local package. Final Devpost submit has not been clicked.

## Product Thesis

Gemini agents can be powerful when they use tools, but operational trust comes from visible tool calls, cost guardrails, evidence, and human approval.

## Current Local Proof

- Terminal agent: `scripts/run_gemini_ops_agent.py`
- Local verifier: `scripts/run_google_local_checks.sh`
- Case data: `case_data/`
- Workflow UI: `prototype/gemini-operations-navigator.html`
- Terminal proof: `prototype/terminal-session.html`
- Tool trace: `reports/mcp-tool-trace.jsonl`
- Cost ledger: `reports/cost-ledger.json`
- Approval checkpoint: `reports/approval-checkpoint.md`
- Demo video: `media/gemini-operations-navigator-demo.mp4`

## Run

```bash
cd /Users/dd/000_AI組織/__hackason/gemini-operations-navigator-public
bash rapid-agent/scripts/run_google_local_checks.sh
```

Expected proof:

```text
google_local_checks_ok
mcp_tool_calls=4
projected_cost_usd=0.021
cost_within_budget=True
human_approval_required=true
```

## Boundary

Safe claim:

- A terminal-executable local Gemini/MCP workflow produces tool trace, cost ledger, approval checkpoint, workflow UI, and natural English demo video.

Do not claim:

- Live Google Cloud deployment.
- Final promotional-credit accounting.
- Unsupervised customer-facing action.
