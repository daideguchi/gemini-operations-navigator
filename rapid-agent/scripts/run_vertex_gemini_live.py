#!/usr/bin/env python3
"""Capture a minimal live Vertex AI Gemini proof without writing secrets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
REPORT_FILE = REPORT_DIR / "vertex-gemini-live-proof.json"
DEFAULT_LOCATION = "us-central1"
DEFAULT_MODELS = ("gemini-2.5-flash", "gemini-2.0-flash-001", "gemini-1.5-flash-002")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def find_auth_cache() -> Path | None:
    configured = os.environ.get("AI_AUTH_CACHE_PATH")
    if configured:
        path = Path(configured).expanduser()
        return path if path.exists() else None

    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "ops" / ".ai_auth_cache.json"
        if candidate.exists():
            return candidate
    return None


def load_auth_defaults() -> dict[str, str]:
    cache_path = find_auth_cache()
    if not cache_path:
        return {}
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}

    section = data.get("google_gemini_hackathon_pj260519", {})
    if not isinstance(section, dict):
        return {}
    defaults: dict[str, str] = {}
    project_id = section.get("project_id")
    credential_path = section.get("service_account_json_path")
    if isinstance(project_id, str) and project_id:
        defaults["project_id"] = project_id
    if isinstance(credential_path, str) and credential_path:
        defaults["credential_path"] = credential_path
    return defaults


def write_report(report: dict[str, Any]) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def skipped_report(reason: str) -> dict[str, Any]:
    return {
        "status": "skipped",
        "captured_at": utc_now(),
        "provider": "Google Cloud Vertex AI",
        "reason": reason,
        "secret_policy": "No service account JSON, OAuth token, API key, or raw credential is written to this report.",
    }


def classify_block(attempts: list[dict[str, Any]]) -> str:
    messages = " ".join(str(attempt.get("error_message", "")) for attempt in attempts).lower()
    if "suspended" in messages:
        return "blocked_by_google_cloud_account_state"
    if "billing" in messages:
        return "blocked_by_billing_state"
    if "quota" in messages or "resource_exhausted" in messages:
        return "blocked_by_quota_state"
    return "failed"


def extract_text(response_json: dict[str, Any]) -> str:
    pieces: list[str] = []
    for candidate in response_json.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            text = part.get("text")
            if isinstance(text, str):
                pieces.append(text)
    return "\n".join(pieces).strip()


def get_access_token(credential_path: Path) -> str:
    from google.auth.transport.requests import Request
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        str(credential_path),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(Request())
    if not credentials.token:
        raise RuntimeError("Google credential refresh returned no access token")
    return str(credentials.token)


def call_vertex(project_id: str, location: str, model: str, token: str, prompt: str) -> tuple[int, dict[str, Any]]:
    import requests

    endpoint = (
        f"https://{location}-aiplatform.googleapis.com/v1/"
        f"projects/{project_id}/locations/{location}/publishers/google/models/{model}:generateContent"
    )
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 96,
        },
    }
    response = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    try:
        body = response.json()
    except ValueError:
        body = {"raw_text_excerpt": response.text[:500]}
    return response.status_code, body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id")
    parser.add_argument("--location", default=os.environ.get("VERTEX_LOCATION", DEFAULT_LOCATION))
    parser.add_argument("--model", default=os.environ.get("VERTEX_MODEL"))
    args = parser.parse_args()

    defaults = load_auth_defaults()
    env_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if env_project_id in {"", "my-gcp-project", "your-project-id"}:
        env_project_id = None
    project_id = args.project_id or defaults.get("project_id") or env_project_id
    credential_path_text = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or defaults.get("credential_path")

    if not project_id:
        report = skipped_report("missing project id; set GOOGLE_CLOUD_PROJECT or AI_AUTH_CACHE_PATH")
        write_report(report)
        print("vertex_gemini_live_status=skipped")
        return
    if not credential_path_text:
        report = skipped_report("missing credentials; set GOOGLE_APPLICATION_CREDENTIALS or AI_AUTH_CACHE_PATH")
        report["project_id"] = project_id
        write_report(report)
        print("vertex_gemini_live_status=skipped")
        return

    credential_path = Path(credential_path_text).expanduser()
    if not credential_path.exists():
        report = skipped_report("credential path does not exist")
        report["project_id"] = project_id
        write_report(report)
        print("vertex_gemini_live_status=skipped")
        return

    prompt = (
        "You are Gemini Operations Navigator. For support ticket CASE-CLOUD-003, "
        "state in one concise sentence why a refund reply must stay blocked until "
        "manager approval, based on policy evidence and cost guardrails."
    )
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]
    models = [args.model] if args.model else list(DEFAULT_MODELS)
    token = get_access_token(credential_path)

    attempts: list[dict[str, Any]] = []
    final_report: dict[str, Any] | None = None
    for model in models:
        http_status, body = call_vertex(project_id, args.location, model, token, prompt)
        text = extract_text(body)
        attempts.append(
            {
                "model": model,
                "http_status": http_status,
                "has_text": bool(text),
                "error_code": body.get("error", {}).get("code") if isinstance(body.get("error"), dict) else None,
                "error_status": body.get("error", {}).get("status") if isinstance(body.get("error"), dict) else None,
                "error_message": body.get("error", {}).get("message", "")[:300]
                if isinstance(body.get("error"), dict)
                else None,
            }
        )
        if http_status == 200 and text:
            usage = body.get("usageMetadata", {})
            final_report = {
                "status": "ok",
                "captured_at": utc_now(),
                "provider": "Google Cloud Vertex AI",
                "project_id": project_id,
                "location": args.location,
                "model": model,
                "endpoint_host": f"{args.location}-aiplatform.googleapis.com",
                "http_status": http_status,
                "prompt_case_id": "CASE-CLOUD-003",
                "prompt_hash": prompt_hash,
                "response_text_excerpt": text[:500],
                "usage_metadata": usage if isinstance(usage, dict) else {},
                "attempts": attempts,
                "claim_boundary": (
                    "Live Vertex AI Gemini generateContent call completed for a support-operations prompt; "
                    "no customer email was sent."
                ),
                "secret_policy": "No service account JSON, OAuth token, API key, or raw credential is written to this report.",
            }
            break

    if final_report is None:
        blocked_status = classify_block(attempts)
        final_report = {
            "status": blocked_status,
            "captured_at": utc_now(),
            "provider": "Google Cloud Vertex AI",
            "project_id": project_id,
            "location": args.location,
            "attempts": attempts,
            "claim_boundary": (
                "No successful live Vertex Gemini generation is claimed from this rerun; "
                "the no-out-of-pocket guardrail blocks billing or credit repair actions."
            ),
            "secret_policy": "No service account JSON, OAuth token, API key, or raw credential is written to this report.",
        }
        write_report(final_report)
        print(f"vertex_gemini_live_status={blocked_status}")
        if blocked_status == "failed":
            raise SystemExit(1)
        return

    write_report(final_report)
    print("vertex_gemini_live_status=ok")
    print(f"vertex_model={final_report['model']}")
    total_tokens = final_report.get("usage_metadata", {}).get("totalTokenCount")
    if total_tokens is not None:
        print(f"vertex_total_tokens={total_tokens}")


if __name__ == "__main__":
    main()
