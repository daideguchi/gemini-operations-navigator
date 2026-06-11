# Manual Devpost Submit Guide — Google Cloud Rapid Agent

Use this if Devpost automation hits reCAPTCHA.

## Links

- Repository: https://github.com/daideguchi/gemini-operations-navigator
- Live demo: https://daideguchi.github.io/gemini-operations-navigator/
- YouTube demo: https://www.youtube.com/watch?v=kt34TmPsT4g
- Submission package: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/SUBMISSION_PACKAGE.md
- Architecture: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/ARCHITECTURE.md
- Terminal proof: https://daideguchi.github.io/gemini-operations-navigator/rapid-agent/prototype/terminal-session.html
- Arize/OpenInference trace: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/openinference-trace.jsonl
- Phoenix MCP runtime proof: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/phoenix-mcp-runtime-proof.json
- Vertex rerun status: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/reports/vertex-gemini-live-proof.json
- Agent Builder manifest: https://raw.githubusercontent.com/daideguchi/gemini-operations-navigator/main/rapid-agent/agent-builder/agent-builder-runtime-manifest.json

## Project Name

```text
Gemini Operations Navigator
```

## Elevator Pitch

```text
Gemini + MCP for support operations managers who need evidence-backed AI drafts, visible cost guardrails, and human approval before customer-facing action.
```

## Inspiration

```text
AI support agents become useful coworkers only when operations managers can see their tools, cost, evidence, and approval boundaries before a customer-facing action.

Gemini Operations Navigator was built around that idea: do not hide the operational controls. Make the agent's workflow understandable before it drafts, escalates, or sends.
```

## What It Does

```text
Gemini Operations Navigator runs a support-operations workflow for refund and escalation queues.

A customer asks for a renewal refund. The agent retrieves the refund policy through an MCP-style tool, checks recent usage, drafts a grounded response with Gemini, records projected cost, exports an Arize/OpenInference-compatible span trace, verifies the Arize Phoenix MCP server interface, and blocks the customer-facing send until a manager approves it.

The demo produces:
- terminal transcript
- MCP tool trace
- Arize/OpenInference-compatible span trace
- cost ledger
- approval checkpoint
- Phoenix MCP runtime proof
- Vertex AI rerun status report
- Agent Builder-ready manifest
- workflow UI
- architecture diagram
- narrated demo video
```

## Built With

```text
Python, HTML, CSS, JSON, JSONL, Gemini-oriented workflow design, MCP-style tool model, Arize Phoenix MCP, Arize/OpenInference-compatible trace export, Google Cloud Agent Builder-ready manifest, ImageMagick, ffmpeg, Edge TTS
```

## Verification Proof

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

## Claim Boundary

```text
This is a verified local workflow prototype with Phoenix MCP runtime proof and an Agent Builder-ready manifest.

It records the current Vertex rerun status and does not claim production Google Cloud deployment, final promotional-credit accounting, or unsupervised customer-facing action.
```
