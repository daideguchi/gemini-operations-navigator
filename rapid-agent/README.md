# Gemini Operations Navigator

Target: Google Cloud Rapid Agent Hackathon

URL: https://rapid-agent.devpost.com/

Status: Devpost joined. P2 large-field lane.

Current local proof:

- Gemini workflow demo: `prototype/gemini-operations-navigator.html`
- Demo screenshot: `media/gemini-operations-navigator-full.png`
- Cost guardrail policy: `reports/cost-guardrail-policy.json`
- Builder: `scripts/build_gemini_workflow_demo.py`

![Gemini Operations Navigator demo](media/gemini-operations-navigator-full.png)

## Position

P2/P3 large-field lane.

This has a large prize pool but very high competition. Use shared engine and Google credits only if cost route is safe.

## Product Thesis

Gemini agents are most useful in operations when they can take action, but every action needs traceability, approval boundaries, and a clear handoff.

Gemini Operations Navigator turns a real operational task into an agent-guided workflow with MCP tool calls, human checkpoints, and evidence-based summaries.

## MVP

- Gemini agent task plan
- one partner MCP tool path
- action log
- human approval checkpoint
- final evidence report
- Google Cloud deployment or demo path

## Shared Engine Use

Reuse:

- agent event schema
- approval gates
- cost signals
- evidence summary

Adapt:

- Gemini calls
- MCP tool calls
- Google Cloud Agent Builder / Vertex path

Current generated artifacts:

- Shared engine: `../shared-agentops-engine/`
- Canonical events: `../shared-agentops-engine/data/agentops_events.jsonl`
- Gemini/MCP workflow plan: `../shared-agentops-engine/adapters/google/gemini_mcp_workflow.json`
- Static dashboard: `../shared-agentops-engine/web/index.html`

Build the Google-focused local demo:

```bash
cd /Users/dd/000_AI組織/__hackason/rapid-agent
python3 scripts/build_gemini_workflow_demo.py
```

Expected proof:

- builder returns `status: ok`
- `prototype/gemini-operations-navigator.html` exists
- `reports/cost-guardrail-policy.json` exists
- screenshot exists at `media/gemini-operations-navigator-full.png`

The Google lane should use DD's free/credit-backed route only after confirming no surprise billing path. Treat cost guardrails as a visible feature, not just an internal note.

## Immediate Next Steps

1. Confirm exact required MCP partner track.
2. Confirm Google credits and no surprise billing route.
3. Select one lightweight support-operations workflow with real demo value.
4. Wire Gemini/MCP actions to the generated AgentOps event stream.

Current boundary:

- Safe claim: a Gemini/MCP workflow prototype, cost guardrail policy, and human approval point are generated from the shared event stream.
- Do not trigger new paid-looking Google/API usage or claim live Google Cloud deployment until the route is verified for the current project.
