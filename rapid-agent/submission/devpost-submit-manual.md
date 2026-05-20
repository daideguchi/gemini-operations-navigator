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

## Project Name

```text
Gemini Operations Navigator
```

## Elevator Pitch

```text
Gemini + MCP for support operations with visible cost guardrails, evidence-backed actions, and human approval checkpoints.
```

## Inspiration

```text
AI agents become useful coworkers only when humans can see their tools, cost, evidence, and approval boundaries.

Gemini Operations Navigator was built around that idea: do not hide the operational controls. Make the agent's workflow understandable before it acts.
```

## What It Does

```text
Gemini Operations Navigator runs a local support-operations workflow.

A customer asks for a renewal refund. The agent retrieves the refund policy through an MCP-style tool, checks recent usage, drafts a grounded response, records projected cost, exports an Arize/OpenInference-compatible span trace, and blocks the customer-facing send until a manager approves it.

The demo produces:
- terminal transcript
- MCP tool trace
- Arize/OpenInference-compatible span trace
- cost ledger
- approval checkpoint
- workflow UI
- architecture diagram
- narrated demo video
```

## Built With

```text
Python, HTML, CSS, JSON, JSONL, Gemini-oriented workflow design, MCP-style tool model, Arize/OpenInference-compatible trace export, Google Cloud / ADK-ready architecture, ImageMagick, ffmpeg, Edge TTS
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
claim_boundary=verified_local_mcp_workflow_no_live_google_deployment_claim
```

## Claim Boundary

```text
This is a verified local workflow prototype.

It does not claim live Google Cloud deployment, final promotional-credit accounting, or unsupervised customer-facing action.
```
