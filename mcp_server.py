#!/usr/bin/env python3
"""agent-vitals as an MCP server: the census, queryable by an agent.

An agent choosing a tool wants to know whether the repository behind it is
still maintained and under what licence. The daily census already answers
that for tens of thousands of repositories; this exposes it over the Model
Context Protocol on stdio, so a client such as Claude Code or Cursor can ask.

Standard library only, like the rest of the repository. Protocol version
2025-06-18, JSON-RPC 2.0 over stdin and stdout, one message per line. Four
tools:

  lookup      one repository by owner/name
  search      repositories by words in the name or description, with filters
  summary     the latest census totals
  candidates  the two acted-on lists: repositories to revive or contribute to

The index is read from data/servers.json next to this file, or from the
published copy on GitHub when AGENT_VITALS_REMOTE=1 is set (one download,
cached for the process). Nothing is written, nothing is executed.

Run it:   python3 mcp_server.py
Client config (Claude Code):
  claude mcp add agent-vitals -- python3 /path/to/agent-vitals/mcp_server.py
"""
from __future__ import annotations

import csv
import io
import json
import os
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REMOTE = "https://raw.githubusercontent.com/Keremozdemirra/agent-vitals/main/data/servers.json"
PROTOCOL = "2025-06-18"
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0", "MPL-2.0", "Unlicense", "0BSD"}

_index: dict | None = None


def index() -> dict:
    global _index
    if _index is None:
        local = HERE / "data" / "servers.json"
        if os.environ.get("AGENT_VITALS_REMOTE") == "1" or not local.exists():
            with urllib.request.urlopen(REMOTE, timeout=60) as r:
                _index = json.load(r)
        else:
            _index = json.loads(local.read_text())
        _index["_by_name"] = {r["full_name"].lower(): r for r in _index["repositories"]}
    return _index


def brief(r: dict) -> dict:
    return {k: r.get(k) for k in ("full_name", "url", "description", "stars", "forks", "open_issues", "language",
                                  "license", "license_state", "status", "days_since_push", "pushed_at", "archived", "is_fork", "topics")}


# ------------------------------------------------------------------ tools

def lookup(full_name: str) -> dict:
    r = index()["_by_name"].get(full_name.strip().lower())
    if not r:
        return {"found": False, "full_name": full_name,
                "note": "Not in the census. The index covers repositories matched by its topic queries with 2+ stars (mcp) or 10+ stars (agents)."}
    return {"found": True, "census_date": index()["generated_at"][:10], "repository": brief(r)}


def search(query: str, status: str | None = None, license: str | None = None, min_stars: int = 0,
           group: str | None = None, limit: int = 20) -> dict:
    words = [w for w in query.lower().split() if w]
    out = []
    for r in index()["repositories"]:
        hay = (r["full_name"] + " " + (r.get("description") or "") + " " + " ".join(r.get("topics") or [])).lower()
        if not all(w in hay for w in words):
            continue
        if status and r["status"] != status:
            continue
        if license == "permissive" and r.get("license") not in PERMISSIVE:
            continue
        if license and license != "permissive" and r.get("license") != license:
            continue
        if group and r.get("group") != group:
            continue
        if r["stars"] < min_stars:
            continue
        out.append(r)
    out.sort(key=lambda r: -r["stars"])
    return {"census_date": index()["generated_at"][:10], "matches": len(out),
            "repositories": [brief(r) for r in out[:max(1, min(limit, 100))]]}


def summary() -> dict:
    ix = index()
    recs = ix["repositories"]
    by = {}
    for r in recs:
        by[r["status"]] = by.get(r["status"], 0) + 1
    lic = sum(1 for r in recs if r.get("license_state") == "none")
    return {"census_date": ix["generated_at"][:10], "repositories": len(recs), "by_status": by,
            "no_licence_file": lic, "groups": ix.get("groups"), "source": "GitHub REST API, public metadata only",
            "statuses": {"active": "pushed within 30 days", "slowing": "31 to 90 days", "stale": "91 to 365 days",
                         "abandoned": "no push in over a year", "archived": "archived on GitHub"}}


def candidates(kind: str = "both", limit: int = 20) -> dict:
    recs = index()["repositories"]
    ok = lambda r: r.get("license") in PERMISSIVE and not r.get("is_fork")
    revive = sorted([r for r in recs if ok(r) and r["status"] in ("abandoned", "archived") and r["stars"] >= 200 and (r.get("open_issues") or 0) >= 5],
                    key=lambda r: -r["stars"])
    contribute = sorted([r for r in recs if ok(r) and r["status"] == "active" and r["stars"] >= 1000 and (r.get("open_issues") or 0) >= 30],
                        key=lambda r: -(r.get("open_issues") or 0))
    out = {"census_date": index()["generated_at"][:10]}
    if kind in ("both", "revive"):
        out["revive"] = {"rule": "no push in over a year or archived, 200+ stars, permissive licence, 5+ open issues",
                         "repositories": [brief(r) for r in revive[:limit]]}
    if kind in ("both", "contribute"):
        out["contribute"] = {"rule": "pushed in 30 days, 1,000+ stars, permissive licence, 30+ open issues",
                             "repositories": [brief(r) for r in contribute[:limit]]}
    return out


TOOLS = [
    {"name": "lookup", "description": "Maintenance status, licence and activity of one GitHub repository from the agent-vitals daily census (MCP servers, agent frameworks, skills).",
     "inputSchema": {"type": "object", "properties": {"full_name": {"type": "string", "description": "owner/name, e.g. modelcontextprotocol/servers"}}, "required": ["full_name"]}},
    {"name": "search", "description": "Search the census by words in the repository name, description or topics, with optional filters, ranked by stars.",
     "inputSchema": {"type": "object", "properties": {
         "query": {"type": "string"},
         "status": {"type": "string", "enum": ["active", "slowing", "stale", "abandoned", "archived"]},
         "license": {"type": "string", "description": "an SPDX id such as MIT, or 'permissive' for any licence a stranger may ship under"},
         "min_stars": {"type": "integer", "minimum": 0},
         "group": {"type": "string", "enum": ["mcp", "agents"]},
         "limit": {"type": "integer", "minimum": 1, "maximum": 100}}, "required": ["query"]}},
    {"name": "summary", "description": "The latest census totals: how many repositories, how many still maintained, how many without a licence file.",
     "inputSchema": {"type": "object", "properties": {}}},
    {"name": "candidates", "description": "Two acted-on lists: quiet permissive repositories still asked about (to revive or fork) and busy permissive ones short of hands (to contribute to).",
     "inputSchema": {"type": "object", "properties": {"kind": {"type": "string", "enum": ["both", "revive", "contribute"]}, "limit": {"type": "integer", "minimum": 1, "maximum": 50}}}},
]

HANDLERS = {"lookup": lookup, "search": search, "summary": summary, "candidates": candidates}


# --------------------------------------------------------------- protocol

def reply(id_, result=None, error=None) -> None:
    msg = {"jsonrpc": "2.0", "id": id_}
    if error is not None:
        msg["error"] = error
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def handle(req: dict) -> None:
    method = req.get("method")
    id_ = req.get("id")
    params = req.get("params") or {}
    if method == "initialize":
        reply(id_, {"protocolVersion": PROTOCOL, "capabilities": {"tools": {}},
                    "serverInfo": {"name": "agent-vitals", "version": "1.0.0",
                                   "description": "A daily census of the AI agent tooling ecosystem on GitHub: what is maintained, what is abandoned, what has no licence."}})
    elif method == "notifications/initialized" or method == "ping" and id_ is None:
        return
    elif method == "ping":
        reply(id_, {})
    elif method == "tools/list":
        reply(id_, {"tools": TOOLS})
    elif method == "tools/call":
        name = params.get("name")
        fn = HANDLERS.get(name)
        if not fn:
            reply(id_, error={"code": -32602, "message": f"unknown tool {name!r}"})
            return
        try:
            result = fn(**(params.get("arguments") or {}))
            reply(id_, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False, indent=1)}], "structuredContent": result, "isError": False})
        except TypeError as e:
            reply(id_, {"content": [{"type": "text", "text": f"bad arguments: {e}"}], "isError": True})
        except Exception as e:  # a network failure on the remote index, most likely
            reply(id_, {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True})
    elif id_ is not None:
        reply(id_, error={"code": -32601, "message": f"method not found: {method}"})


def main() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            reply(None, error={"code": -32700, "message": "parse error"})
            continue
        handle(req)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
