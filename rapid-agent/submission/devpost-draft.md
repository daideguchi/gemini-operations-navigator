# Devpost Draft — Gemini Operations Navigator

## Tagline

Gemini + MCP for support operations with human approval and visible cost guardrails.

## What It Does

Gemini Operations Navigator helps a support manager run an agent-guided workflow without losing control of cost, evidence, or escalation.

The prototype shows:

- a Gemini agent plan
- policy retrieval through an MCP-style tool
- a grounded draft answer
- a cost signal
- a human approval checkpoint
- a final handoff event

## Demo Story

A support manager wants an agent that can answer customer questions and escalate uncertain cases.

The agent retrieves current policy, drafts a grounded response, and then detects that high-quality model usage should be reserved for escalations. The workflow pauses at a human approval point, where the manager approves an escalation-only budget mode.

## Why It Matters

Fast agents are not enough for operations. Teams need agents that can act with tools, cite evidence, and stay inside budget boundaries.

This project treats cost control and human approval as first-class workflow features rather than hidden implementation details.

## Built With

- Shared AgentOps event stream
- Gemini/MCP workflow specification
- Local HTML demo artifact
- Cost guardrail policy JSON

Current local artifacts:

- `prototype/gemini-operations-navigator.html`
- `media/gemini-operations-navigator-full.png`
- `reports/cost-guardrail-policy.json`
- `../shared-agentops-engine/adapters/google/gemini_mcp_workflow.json`

## Claim Boundary

This is currently a local workflow prototype generated from the shared event stream.

Do not claim live Google Cloud deployment or new live Gemini calls until the billing/credit route is verified for the current project.
