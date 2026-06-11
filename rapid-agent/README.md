# Gemini Operations Navigator

Target: Google Cloud Rapid Agent Hackathon

Status: submission package with runtime proof files. Devpost fields should be re-saved after the latest proof update.

## Product Thesis

Gemini agents can be powerful when they use tools, but support operations managers need visible tool calls, cost guardrails, evidence, observability, and human approval before a refund reply reaches a customer.

## Current Local Proof

- Terminal agent: `scripts/run_gemini_ops_agent.py`
- Local verifier: `scripts/run_google_local_checks.sh`
- Case data: `case_data/`
- Workflow UI: `prototype/gemini-operations-navigator.html`
- Terminal proof: `prototype/terminal-session.html`
- Tool trace: `reports/mcp-tool-trace.jsonl`
- Cost ledger: `reports/cost-ledger.json`
- Approval checkpoint: `reports/approval-checkpoint.md`
- Vertex rerun status: `reports/vertex-gemini-live-proof.json`
- Phoenix MCP proof: `reports/phoenix-mcp-runtime-proof.json`
- Agent Builder manifest: `agent-builder/agent-builder-runtime-manifest.json`
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
vertex_status=blocked_by_google_cloud_account_state
phoenix_mcp_tool_count=27
agent_builder_manifest=present
```

## Boundary

Safe claim:

- A terminal-executable Gemini/MCP workflow produces tool trace, cost ledger, approval checkpoint, workflow UI, Phoenix MCP runtime proof, Agent Builder-ready manifest, and natural English demo video.
- The current Vertex rerun status is recorded truthfully.

Do not claim:

- Production Google Cloud deployment.
- Final promotional-credit accounting.
- Unsupervised customer-facing action.
