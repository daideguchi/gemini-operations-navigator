# Architecture — Gemini Operations Navigator

## One Sentence

Gemini Operations Navigator is a Google Rapid Agent workflow for support
operations managers. It makes Gemini drafting, MCP tool use, Phoenix
observability, cost guardrails, and human approval visible before an agent
takes customer-facing action.

## Data Flow

```text
Support ticket + policy excerpt + tool catalog
        |
        v
Local Gemini/MCP workflow runner + Agent Builder-ready manifest
        |
        +--> policy_mcp.retrieve_refund_policy
        +--> billing_mcp.check_recent_usage
        +--> gemini.generate_grounded_draft
        +--> gmail_mcp.send_customer_reply blocked until approval
        +--> phoenix-mcp stdio initialize/tools.list proof
        +--> vertex generateContent rerun status report
        |
        v
Outputs
  terminal transcript
  MCP tool trace
  cost ledger
  approval checkpoint
  Phoenix MCP runtime proof
  Vertex AI rerun status
  Agent Builder-ready runtime manifest
  workflow UI
  demo video
```

## Human-AI Boundary

The agent can retrieve policy, check usage, draft a grounded reply, estimate
cost, and prepare an escalation. It cannot send a customer-facing financial
answer without human approval.

## Cost Boundary

The local run uses a `0.05 USD` prototype budget and stops/downgrades if the
projected tool/model path exceeds that budget.

## Submission Boundary

This repository claims a verified local Gemini/MCP workflow prototype, actual
Phoenix MCP runtime proof, and an Agent Builder-ready manifest. It records the
current Vertex AI rerun status and does not claim production Google Cloud
deployment, final promotional-credit accounting, or unsupervised
customer-facing action.
