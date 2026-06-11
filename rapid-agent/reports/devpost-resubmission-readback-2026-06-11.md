# Devpost Resubmission Readback — 2026-06-11

## Submission

- Hackathon: Google Cloud Rapid Agent Hackathon
- Project: Gemini Operations Navigator
- Devpost URL: https://devpost.com/software/gemini-operations-navigator
- Manage readback: `SUBMITTED`, `5/5 steps done`, `Project submitted!`
- Commit pushed before readback: `4fcdaf9 Strengthen rapid agent submission proof`

## Public Page Readback

The public Devpost page now shows:

```text
Auditable Gemini support workflow for refund managers with MCP evidence, Phoenix traces, cost guardrails, and approval gates.
```

The public story now includes:

```text
support operations managers handling refund and escalation queues
Arize Phoenix MCP server over stdio
Agent Builder-ready runtime manifest
Vertex AI rerun status report
```

## Linked Proof Surfaces

- Public review hub: https://daideguchi.github.io/gemini-operations-navigator/
- Phoenix MCP proof: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/phoenix-mcp-runtime-proof.json
- Vertex rerun status: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/vertex-gemini-live-proof.json
- Agent Builder manifest: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/agent-builder/agent-builder-runtime-manifest.json

## Boundary

The resubmission does not claim a successful live Vertex generation or production Google Cloud deployment from the latest rerun. The current Vertex report records the real Google Cloud stopline:

```text
blocked_by_google_cloud_account_state
Permission denied: Consumer 'projects/pj260519' has been suspended.
```
