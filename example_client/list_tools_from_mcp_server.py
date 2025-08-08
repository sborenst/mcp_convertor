#!/usr/bin/env python3
# Simple MCP tools lister (no classes/functions)

import os
import json
import sys
import requests
from dotenv import load_dotenv
from openai import OpenAI

# --- Config (edit these) ---
MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", "9000"))
MCP_BASE = f"http://{MCP_HOST}:{MCP_PORT}/mcp/"

# Optional: OpenAI-protocol LLM using Gemini key (not used yet, for future steps)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_APIKEY") or os.getenv("GEMINI_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env (LLM not used yet)")

# You can point this OpenAI-compatible client to any base_url that supports OpenAI API
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api")  # example
MODEL = os.getenv("MODEL", "google/gemini-2.0-flash-exp")

# Initialize OpenAI-protocol client (not used yet)
try:
    llm = OpenAI(api_key=GEMINI_API_KEY, base_url=OPENAI_BASE_URL)
except Exception as e:
    print(f"Note: LLM client init failed (ok for now): {e}")

# --- HTTP headers for MCP ---
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}

# 1) Initialize session
init_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {"tools": {}},
        "clientInfo": {"name": "simple-tools-list", "version": "0.1"},
    },
}

try:
    resp = requests.post(MCP_BASE, headers=headers, data=json.dumps(init_payload), timeout=10, stream=True)
except Exception as e:
    print(f"Failed to reach MCP server at {MCP_BASE}: {e}")
    sys.exit(1)

if resp.status_code in (301, 302, 307, 308) and resp.headers.get("Location"):
    # Follow redirect once if needed
    MCP_BASE = resp.headers["Location"].rstrip("/") + "/"
    resp = requests.post(MCP_BASE, headers=headers, data=json.dumps(init_payload), timeout=10, stream=True)

if resp.status_code != 200:
    print(f"Initialize failed: HTTP {resp.status_code} - {resp.text}")
    sys.exit(1)

session_id = resp.headers.get("mcp-session-id") or resp.headers.get("Mcp-Session-Id")
if not session_id:
    print("No mcp-session-id header returned from initialize")
    sys.exit(1)
print(f"Session established: {session_id}")

# 2) Send required notification
notify_headers = dict(headers)
notify_headers["Mcp-Session-Id"] = session_id
notify_payload = {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}

r = requests.post(MCP_BASE, headers=notify_headers, data=json.dumps(notify_payload), timeout=10)
if r.status_code not in (200, 202):
    print(f"notifications/initialized failed: HTTP {r.status_code} - {r.text}")
    # Continue anyway; some servers return 202

# 3) List tools
list_payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}

resp = requests.post(MCP_BASE, headers=notify_headers, data=json.dumps(list_payload), timeout=20, stream=True)
if resp.status_code != 200:
    print(f"tools/list failed: HTTP {resp.status_code} - {resp.text}")
    sys.exit(1)

# Parse SSE stream and print tools
printed_any = False
for raw in resp.iter_lines(decode_unicode=True):
    if not raw:
        continue
    if raw.startswith("data: "):
        data = raw[6:]
        if data == "[DONE]":
            break
        try:
            msg = json.loads(data)
        except Exception:
            continue
        result = msg.get("result") or {}
        tools = result.get("tools")
        if tools:
            printed_any = True
            print("Available tools:")
            for t in tools:
                name = t.get("name", "<unknown>")
                desc = (t.get("description") or "").strip().splitlines()[0] if t.get("description") else ""
                print(f"- {name}: {desc}")
            break

if not printed_any:
    print("No tools received (check server logs).") 