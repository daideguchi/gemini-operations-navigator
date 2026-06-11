#!/usr/bin/env node
import { spawn } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const ROOT = path.resolve(path.dirname(__filename), "..");
const REPORT_DIR = path.join(ROOT, "reports");
const REPORT_FILE = path.join(REPORT_DIR, "phoenix-mcp-runtime-proof.json");
const PACKAGE_NAME = "@arizeai/phoenix-mcp@latest";

function nowIso() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

async function writeReport(report) {
  await mkdir(REPORT_DIR, { recursive: true });
  await writeFile(REPORT_FILE, `${JSON.stringify(report, null, 2)}\n`, "utf8");
}

function compactError(error) {
  if (!error) return null;
  return {
    code: error.code ?? null,
    message: String(error.message ?? error).slice(0, 500),
  };
}

async function main() {
  const child = spawn("npx", ["-y", PACKAGE_NAME], {
    stdio: ["pipe", "pipe", "pipe"],
    env: {
      ...process.env,
      NO_COLOR: "1",
    },
  });

  let nextId = 1;
  let stdoutBuffer = "";
  let stderrText = "";
  const pending = new Map();
  const nonJsonLines = [];

  const failAll = (error) => {
    for (const { reject, timer } of pending.values()) {
      clearTimeout(timer);
      reject(error);
    }
    pending.clear();
  };

  child.stdout.on("data", (chunk) => {
    stdoutBuffer += chunk.toString("utf8");
    let lineBreak;
    while ((lineBreak = stdoutBuffer.indexOf("\n")) >= 0) {
      const line = stdoutBuffer.slice(0, lineBreak).trim();
      stdoutBuffer = stdoutBuffer.slice(lineBreak + 1);
      if (!line) continue;
      try {
        const message = JSON.parse(line);
        if (message.id && pending.has(message.id)) {
          const { resolve, timer } = pending.get(message.id);
          pending.delete(message.id);
          clearTimeout(timer);
          resolve(message);
        }
      } catch {
        nonJsonLines.push(line.slice(0, 300));
      }
    }
  });

  child.stderr.on("data", (chunk) => {
    stderrText += chunk.toString("utf8");
  });

  child.on("error", (error) => {
    failAll(error);
  });

  function send(message) {
    child.stdin.write(`${JSON.stringify(message)}\n`);
  }

  function request(method, params = {}, timeoutMs = 20000) {
    const id = nextId++;
    const promise = new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        pending.delete(id);
        reject(new Error(`${method} timed out after ${timeoutMs}ms`));
      }, timeoutMs);
      pending.set(id, { resolve, reject, timer });
    });
    send({ jsonrpc: "2.0", id, method, params });
    return promise;
  }

  let report;
  try {
    const initialize = await request("initialize", {
      protocolVersion: "2024-11-05",
      capabilities: {},
      clientInfo: {
        name: "gemini-operations-navigator-proof",
        version: "1.0.0",
      },
    });
    send({ jsonrpc: "2.0", method: "notifications/initialized", params: {} });

    const tools = await request("tools/list", {}, 20000);
    const toolList = tools.result?.tools ?? [];
    const toolNames = toolList.map((tool) => tool.name).filter(Boolean);
    const selectedToolNames = [
      "list-projects",
      "list-traces",
      "get-spans",
      "phoenix-support",
    ].filter((name) => toolNames.includes(name));

    let supportCall = { status: "not_run" };
    if (toolNames.includes("phoenix-support")) {
      try {
        const support = await request(
          "tools/call",
          {
            name: "phoenix-support",
            arguments: {
              query: "Which Phoenix MCP tools should inspect traces and spans for a support operations agent?",
            },
          },
          15000,
        );
        supportCall = {
          status: support.error ? "error" : "ok",
          error: compactError(support.error),
          content_excerpt: JSON.stringify(support.result ?? {}).slice(0, 500),
        };
      } catch (error) {
        supportCall = {
          status: "timeout_or_unavailable",
          error: compactError(error),
        };
      }
    }

    report = {
      status: toolList.length > 0 ? "ok" : "failed",
      captured_at: nowIso(),
      partner_track: "Arize",
      mcp_server_package: PACKAGE_NAME,
      server_info: initialize.result?.serverInfo ?? {},
      protocol_version: initialize.result?.protocolVersion ?? null,
      tool_count: toolList.length,
      selected_tools: selectedToolNames,
      tool_sample: toolNames.slice(0, 18),
      support_call: supportCall,
      non_json_stdout_lines: nonJsonLines.slice(0, 5),
      stderr_excerpt: stderrText.trim().slice(0, 500),
      claim_boundary:
        "An actual Arize Phoenix MCP server process launched over stdio and answered " +
        "JSON-RPC initialize/tools.list for this runtime proof.",
    };
  } catch (error) {
    report = {
      status: "failed",
      captured_at: nowIso(),
      partner_track: "Arize",
      mcp_server_package: PACKAGE_NAME,
      error: compactError(error),
      stderr_excerpt: stderrText.trim().slice(0, 500),
      claim_boundary: "No Phoenix MCP runtime proof was captured.",
    };
  } finally {
    child.stdin.end();
    child.kill();
  }

  await writeReport(report);
  console.log(`phoenix_mcp_status=${report.status}`);
  if (report.status !== "ok") {
    process.exitCode = 1;
  } else {
    console.log(`phoenix_mcp_tool_count=${report.tool_count}`);
    console.log(`phoenix_mcp_selected_tools=${report.selected_tools.join(",")}`);
  }
}

main().catch(async (error) => {
  await writeReport({
    status: "failed",
    captured_at: nowIso(),
    partner_track: "Arize",
    mcp_server_package: PACKAGE_NAME,
    error: compactError(error),
    claim_boundary: "Unexpected probe failure.",
  });
  console.error(error);
  process.exit(1);
});
