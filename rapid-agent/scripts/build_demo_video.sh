#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$ROOT/.." && pwd)"
FONT="/System/Library/Fonts/Supplemental/Arial.ttf"
MONO_FONT="/System/Library/Fonts/Menlo.ttc"
EDGE_TTS_PYTHON="${EDGE_TTS_PYTHON:-python3.11}"
EDGE_TTS_VOICE="${EDGE_TTS_VOICE:-en-US-AvaNeural}"
EDGE_TTS_RATE="${EDGE_TTS_RATE:--7%}"
OUT="$ROOT/media/gemini-operations-navigator-demo.mp4"
LEGACY_OUT="$ROOT/media/gemini-operations-navigator-demo-draft.mp4"
TMP_DIR="$ROOT/media/.demo_video_tmp"

rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

if [ ! -s "$ROOT/reports/terminal-transcript.txt" ]; then
  python3 "$ROOT/scripts/run_gemini_ops_agent.py" >/dev/null
fi

make_screenshot_slide() {
  local src="$1"
  local title="$2"
  local subtitle="$3"
  local out="$4"
  magick "$src" \
    -resize 1920x \
    -crop 1920x1080+0+0 +repage \
    -fill "#000000B8" -draw "rectangle 0,810 1920,1080" \
    -font "$FONT" -fill white -pointsize 58 -annotate +72+900 "$title" \
    -font "$FONT" -fill white -pointsize 34 -annotate +72+980 "$subtitle" \
    "$out"
}

make_text_slide() {
  local title="$1"
  local subtitle="$2"
  local body="$3"
  local out="$4"
  magick -size 1920x1080 xc:"#f6f7fb" \
    -fill "#1a73e8" -draw "rectangle 0,0 1920,260" \
    -fill "#ffffff" -font "$FONT" -pointsize 72 -annotate +82+150 "$title" \
    -fill "#e8f0fe" -font "$FONT" -pointsize 34 -annotate +86+218 "$subtitle" \
    -fill "#ffffff" -stroke "#d8e0ea" -strokewidth 3 -draw "roundrectangle 120,410 1800,760 24,24" \
    -stroke none -fill "#1f2937" -font "$FONT" -pointsize 46 -annotate +170+520 "$body" \
    -fill "#667085" -font "$FONT" -pointsize 28 -annotate +170+640 "The agent is useful because tool use, spend, and approval are visible before action." \
    "$out"
}

make_terminal_slide() {
  local out="$1"
  magick -size 1920x1080 xc:"#0b1220" \
    -fill "#1f2937" -draw "roundrectangle 90,80 1830,980 18,18" \
    -fill "#111827" -draw "rectangle 90,80 1830,148" \
    -fill "#f8fafc" -font "$FONT" -pointsize 30 -annotate +130+124 "CASE-CLOUD-003 · Gemini/MCP terminal run" \
    -fill "#bfdbfe" -font "$MONO_FONT" -pointsize 30 -annotate +130+220 "$ python3 rapid-agent/scripts/run_gemini_ops_agent.py" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+285 "[tool] policy_mcp.retrieve_refund_policy: success · kb-refund-2026-05" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+340 "[tool] billing_mcp.check_recent_usage: success · usage-sup-1042" \
    -fill "#dbeafe" -font "$MONO_FONT" -pointsize 28 -annotate +130+395 "[tool] gemini.generate_grounded_draft: success · draft-sup-1042" \
    -fill "#fecaca" -font "$MONO_FONT" -pointsize 28 -annotate +130+450 "[tool] gmail_mcp.send_customer_reply: blocked_pending_human_approval" \
    -fill "#bbf7d0" -font "$MONO_FONT" -pointsize 28 -annotate +130+530 "[cost] projected=$0.021 within_budget=True" \
    -fill "#fde68a" -font "$MONO_FONT" -pointsize 28 -annotate +130+585 "[approval] customer-facing send is blocked until manager approval" \
    -fill "#93c5fd" -font "$MONO_FONT" -pointsize 28 -annotate +130+650 "[boundary] verified local MCP workflow; no live deployment claimed" \
    "$out"
}

cat > "$TMP_DIR/narration.txt" <<'TEXT'
Gemini Operations Navigator is a cost-aware, approval-first agent workflow for the Google Cloud Rapid Agent Hackathon.

The idea is not to let an AI do everything. The idea is to give Gemini a clear operating lane: use MCP-style tools, cite policy, watch cost, and stop before a risky customer-facing action.

This demo runs a local support ticket. A customer asks for a renewal refund. The agent retrieves the refund policy, checks recent usage, drafts a grounded response, and records the cost of the workflow.

Then the most important part happens. Sending the customer reply is blocked, because it is a financial answer that needs manager approval.

The dashboard and terminal proof show the same principle: Gemini can plan and draft, but tool calls, spend, evidence, and approval gates stay visible to the human operator.

This submission is honest about its boundary. It is a verified local MCP workflow with a Google-ready architecture. It does not claim live Google Cloud deployment or final promotional-credit accounting.
TEXT

"$EDGE_TTS_PYTHON" -m edge_tts \
  --voice "$EDGE_TTS_VOICE" \
  --rate="$EDGE_TTS_RATE" \
  --file "$TMP_DIR/narration.txt" \
  --write-media "$TMP_DIR/narration.mp3"

make_text_slide \
  "Gemini Operations Navigator" \
  "Gemini + MCP tools with cost and approval control" \
  "A support agent should know when to stop before action." \
  "$TMP_DIR/slide-0.png"

make_terminal_slide "$TMP_DIR/slide-1.png"

make_screenshot_slide "$ROOT/media/gemini-operations-navigator-full.png" \
  "Workflow Review Surface" \
  "MCP tools, cost signals, and human checkpoints stay visible." \
  "$TMP_DIR/slide-2.png"

make_screenshot_slide "$REPO_ROOT/shared-agentops-engine/media/shared-dashboard-full.png" \
  "AgentOps Timeline" \
  "Human, AI, API, and approval events can be reviewed together." \
  "$TMP_DIR/slide-3.png"

make_text_slide \
  "Cost Is A Product Feature" \
  "The local run stays under a 5 cent prototype budget" \
  "Extra model/tool loops are blocked before spend becomes invisible." \
  "$TMP_DIR/slide-4.png"

make_screenshot_slide "$ROOT/media/gemini-operations-navigator-full.png" \
  "Honest Submission Boundary" \
  "Verified local workflow. Live Google Cloud deployment is not claimed yet." \
  "$TMP_DIR/slide-5.png"

ffmpeg -y \
  -loop 1 -t 14 -i "$TMP_DIR/slide-0.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-1.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-2.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-3.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-4.png" \
  -loop 1 -t 14 -i "$TMP_DIR/slide-5.png" \
  -i "$TMP_DIR/narration.mp3" \
  -filter_complex "[0:v][1:v][2:v][3:v][4:v][5:v]concat=n=6:v=1:a=0,format=yuv420p[v];[6:a]loudnorm=I=-16:TP=-1.5:LRA=11,volume=0.85[a]" \
  -map "[v]" -map "[a]" -r 30 -shortest -movflags +faststart "$OUT"

cp "$OUT" "$LEGACY_OUT"
rm -rf "$TMP_DIR"
echo "$OUT"
