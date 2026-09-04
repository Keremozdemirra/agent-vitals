#!/usr/bin/env python3
"""Collect a daily census of the MCP / agent-tooling ecosystem from the GitHub API.

Standard library only. Reads GITHUB_TOKEN from the environment when present
(raising the search rate limit); the token is never written anywhere.

Only public repository metadata is recorded: names, dates, licence fields and
counts. No repository is cloned, no file is downloaded, no code is executed.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DAILY = DATA / "daily"
API = "https://api.github.com/search/repositories"
UA = "agent-vitals (+https://github.com/Keremozdemirra/agent-vitals)"

# Each query is capped by GitHub at 1000 results, so every query is sliced by
# star count until each slice fits under the cap. That is what makes this a
# census rather than a top-1000 sample.
# Two tiers, because one star floor cannot serve both halves of this subject.
#
# The MCP topics name a specific thing, so two stars is enough to mean "someone
# other than the author noticed". The broad agent topics are also attached to
# every tutorial, course repo and fork in the field; at two stars they return
# 100k results, drown the signal and push the run past four hours. Ten stars is
# where those topics start describing tools rather than exercises.
#
# The floor per group is published in the data. Changing one changes every
# headline number, so it is a stated parameter, not a tuning knob.
GROUPS = [
    ("mcp", 2, [
        "topic:mcp-server",
        "topic:model-context-protocol",
    ]),
    ("agents", 10, [
        "topic:mcp",
        "topic:claude-code",
        "topic:ai-agents",
        "topic:ai-agent",
        "topic:agent-skills",
        "topic:agentic-ai",
        "topic:claude-skills",
        "topic:autonomous-agents",
        "topic:llm-agents",
        "topic:agent-framework",
        "topic:llm-tools",
    ]),
]

QUERIES = [q for _, _, qs in GROUPS for q in qs]

EPOCH = dt.date(2008, 1, 1)
TODAY = dt.date.today().isoformat()
PAGE_CAP = 1000  # GitHub returns no more than 1000 results for one query


def api_get(url: str, attempt: int = 0) -> dict:
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": UA,
        "X-GitHub-Api-Version": "2022-11-28",
    })
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # 403/429 here is secondary rate limiting, not a permissions problem.
        if exc.code in (403, 429) and attempt < 5:
            wait = int(exc.headers.get("Retry-After") or (2 ** attempt) * 15)
            print(f"    rate limited, waiting {wait}s", file=sys.stderr)
            time.sleep(min(wait, 120))
            return api_get(url, attempt + 1)
        raise
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        if attempt < 4:
            time.sleep((2 ** attempt) * 5)
            return api_get(url, attempt + 1)
        raise


def note(errors: list, message: str) -> None:
    """Record an error and say so immediately. Silence during a 20-minute
    unattended run is indistinguishable from progress."""
    errors.append(message)
    print(f"    ERROR {message}", file=sys.stderr)


def search_url(query: str, page: int) -> str:
    return f"{API}?q={urllib.parse.quote(query)}&per_page=100&page={page}&sort=updated"


def star_term(lo: int, hi: int | None) -> str:
    if hi is None:
        return f"stars:>={lo}"
    return f"stars:{lo}..{hi}" if hi > lo else f"stars:{lo}"


def date_term(lo: dt.date, hi: dt.date) -> str:
    return f"created:{lo.isoformat()}..{hi.isoformat()}"


def collect_pages(query: str, first: dict, found: dict, errors: list) -> None:
    """Drain a query already known to fit under the 1000-result ceiling."""
    for item in first.get("items", []):
        found[item["full_name"]] = item
    total = first.get("total_count", 0)
    pages = min((total + 99) // 100, 10)
    for page in range(2, pages + 1):
        time.sleep(2.2)  # authenticated search allows 30 requests/minute
        try:
            payload = api_get(search_url(query, page))
        except Exception as exc:
            note(errors, f"{query} page {page}: {type(exc).__name__}: {exc}")
            return
        for item in payload.get("items", []):
            found[item["full_name"]] = item


def harvest(base: str, stars: tuple[int, int | None], dates: tuple[dt.date, dt.date] | None,
            found: dict, errors: list, depth: int = 0) -> None:
    """Recursively narrow a query until every slice fits under the result cap.

    Stars are bisected first because they are cheap to split. When a slice
    collapses to a single star value that still overflows, creation date
    becomes the second axis. This is what makes the result a census rather
    than a top-1000 sample.
    """
    lo, hi = stars
    query = f"{base} {star_term(lo, hi)}"
    if dates:
        query += " " + date_term(*dates)

    time.sleep(2.2)
    try:
        first = api_get(search_url(query, 1))
    except Exception as exc:
        note(errors, f"{query}: {type(exc).__name__}: {exc}")
        return

    total = first.get("total_count", 0)
    if total == 0:
        return
    if total <= PAGE_CAP:
        collect_pages(query, first, found, errors)
        return
    if depth >= 16:
        note(errors, f"slice not exhaustive after {depth} splits: '{query}' has {total}")
        collect_pages(query, first, found, errors)
        return

    if hi is None:
        # Open-ended top slice: cut it at double the floor and recurse both ways.
        mid = max(lo * 2, lo + 1)
        harvest(base, (lo, mid - 1), dates, found, errors, depth + 1)
        harvest(base, (mid, None), dates, found, errors, depth + 1)
    elif hi > lo:
        mid = (lo + hi) // 2
        harvest(base, (lo, mid), dates, found, errors, depth + 1)
        harvest(base, (mid + 1, hi), dates, found, errors, depth + 1)
    else:
        # One star value, still over the cap: split on creation date instead.
        d_lo, d_hi = dates or (EPOCH, dt.date.today())
        if (d_hi - d_lo).days <= 1:
            note(errors, f"slice not exhaustive: '{query}' has {total}")
            collect_pages(query, first, found, errors)
            return
        mid = d_lo + (d_hi - d_lo) / 2
        harvest(base, stars, (d_lo, mid), found, errors, depth + 1)
        harvest(base, stars, (mid + dt.timedelta(days=1), d_hi), found, errors, depth + 1)


def load_denylist() -> set[str]:
    """Repositories whose owners asked for their description not to be published.

    They stay in the census — removing them would quietly falsify the counts —
    but their description field is emptied.
    """
    path = ROOT / "denylist.txt"
    if not path.exists():
        return set()
    names = set()
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            names.add(line.lower())
    return names


def clean(text: str | None, limit: int = 300) -> str:
    """Repository descriptions are written by third parties: treat as untrusted.

    Control characters are stripped and the string is truncated. Escaping for
    the output format happens at render time, never here.
    """
    if not text:
        return ""
    flat = "".join(ch if (ch == " " or ch.isprintable()) else " " for ch in text)
    flat = " ".join(flat.split())
    return flat[:limit]


def bucket(days: int | None, archived: bool) -> str:
    if archived:
        return "archived"
    if days is None:
        return "unknown"
    if days <= 30:
        return "active"
    if days <= 90:
        return "slowing"
    if days <= 365:
        return "stale"
    return "abandoned"


def days_since(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        when = dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
    except ValueError:
        return None
    return (dt.date.today() - when).days


def main() -> int:
    DAILY.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []

    previous: dict[str, dict] = {}
    loaded: dict = {}
    prior_path = DATA / "servers.json"
    if prior_path.exists():
        loaded = json.loads(prior_path.read_text())
        previous = {r["full_name"]: r for r in loaded.get("repositories", [])}

    try:
        probe = api_get(search_url(f"{GROUPS[0][2][0]} {star_term(GROUPS[0][1], None)}", 1))
        if not probe.get("items"):
            print("pre-flight returned no items; aborting before the long run",
                  file=sys.stderr)
            return 1
    except Exception as exc:
        print(f"pre-flight failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    raw: dict[str, dict] = {}
    group_of: dict[str, str] = {}
    for group, floor, queries in GROUPS:
        for query in queries:
            print(f"query: {query} (stars >= {floor})", file=sys.stderr)
            before = set(raw)
            harvest(query, (floor, None), None, raw, errors)
            for name in set(raw) - before:
                group_of.setdefault(name, group)
            print(f"  running total: {len(raw)}", file=sys.stderr)

    if not raw:
        print("collected nothing; refusing to overwrite the index", file=sys.stderr)
        return 1

    denied = load_denylist()
    if denied:
        print(f"denylist: {len(denied)} description(s) suppressed", file=sys.stderr)

    records = []
    for full_name, item in sorted(raw.items()):
        pushed = item.get("pushed_at")
        age = days_since(pushed)
        # Three distinct states, and collapsing them libels people. A null
        # licence object means no licence file was found: exclusive copyright
        # by default. NOASSERTION means a licence file exists that GitHub
        # cannot map to a standard identifier — n8n's Sustainable Use License
        # lands here, and it is emphatically not "no licence".
        lic_obj = item.get("license") or {}
        spdx = lic_obj.get("spdx_id")
        if not lic_obj:
            licence, licence_state = None, "none"
        elif spdx in ("NOASSERTION", None, ""):
            licence, licence_state = None, "non-standard"
        else:
            licence, licence_state = spdx, "spdx"
        prior = previous.get(full_name)
        records.append({
            "full_name": full_name,
            "group": group_of.get(full_name, "agents"),
            "url": item.get("html_url", ""),
            "description": "" if full_name.lower() in denied
                           else clean(item.get("description")),
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "open_issues": item.get("open_issues_count", 0),
            "language": item.get("language") or "",
            "topics": sorted(item.get("topics", []))[:12],
            "license": licence,
            "license_state": licence_state,
            "archived": bool(item.get("archived")),
            "is_fork": bool(item.get("fork")),
            "created_at": (item.get("created_at") or "")[:10],
            "pushed_at": (pushed or "")[:10],
            "days_since_push": age,
            "status": bucket(age, bool(item.get("archived"))),
            "first_seen": (prior or {}).get("first_seen", TODAY),
            "last_seen": TODAY,
        })

    by_status: dict[str, int] = {}
    for rec in records:
        by_status[rec["status"]] = by_status.get(rec["status"], 0) + 1

    # A repository created four months ago cannot be a year stale. Reporting
    # the raw abandoned share of a young ecosystem understates it by a factor
    # of three; the honest denominator is the repositories old enough to
    # qualify.
    eligible = [r for r in records
                if r["created_at"] and days_since(r["created_at"]) is not None
                and days_since(r["created_at"]) >= 365]
    eligible_abandoned = [r for r in eligible if r["status"] == "abandoned"]

    no_licence = [r for r in records if r["license_state"] == "none"]
    nonstandard = [r for r in records if r["license_state"] == "non-standard"]
    licences: dict[str, int] = {}
    for rec in records:
        key = {"none": "no licence file",
               "non-standard": "licence GitHub cannot identify"}.get(
                   rec["license_state"], rec["license"])
        licences[key] = licences.get(key, 0) + 1

    prior_groups = (loaded.get("groups") if prior_path.exists() else None) or {}
    now_groups = {name: {"min_stars": floor, "queries": qs}
                  for name, floor, qs in GROUPS}
    scope_changed = bool(prior_groups) and prior_groups != now_groups
    if scope_changed:
        print("scope changed since the last run; churn is not comparable",
              file=sys.stderr)

    seen_now = set(raw)
    seen_before = set(previous)
    arrivals = sorted(seen_now - seen_before)
    departures = sorted(seen_before - seen_now)

    newly_abandoned = sorted(
        r["full_name"] for r in records
        if r["status"] == "abandoned"
        and previous.get(r["full_name"], {}).get("status") not in (None, "abandoned")
    )
    newly_archived = sorted(
        r["full_name"] for r in records
        if r["archived"] and not previous.get(r["full_name"], {}).get("archived", False)
    )

    snapshot = {
        "date": TODAY,
        "groups": {name: floor for name, floor, _ in GROUPS},
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "status": "partial" if errors else "complete",
        "totals": {
            "repositories": len(records),
            "stars": sum(r["stars"] for r in records),
            "no_licence": len(no_licence),
            "no_licence_pct": round(100 * len(no_licence) / len(records), 1),
            "nonstandard_licence": len(nonstandard),
            "nonstandard_licence_pct": round(100 * len(nonstandard) / len(records), 1),
            "abandoned_pct": round(100 * by_status.get("abandoned", 0) / len(records), 1),
            "active_pct": round(100 * by_status.get("active", 0) / len(records), 1),
            "old_enough_to_be_abandoned": len(eligible),
            "abandoned_of_eligible_pct": round(
                100 * len(eligible_abandoned) / max(len(eligible), 1), 1),
        },
        "by_status": dict(sorted(by_status.items())),
        "by_group": {name: sum(1 for r in records if r["group"] == name)
                     for name, _, _ in GROUPS},
        "by_license": dict(sorted(licences.items(), key=lambda kv: -kv[1])[:15]),
        "churn": {
            "arrived": arrivals[:200],
            "arrived_count": len(arrivals),
            "left_the_index": departures[:200],
            "left_count": len(departures),
            "newly_abandoned": newly_abandoned[:100],
            "newly_archived": newly_archived[:100],
            "first_run": not previous,
            "scope_changed": scope_changed,
            "previous_scope": {k: v.get("min_stars") for k, v in prior_groups.items()},
        },
        "errors": errors[:25],
    }

    index = {
        "generated_at": snapshot["generated_at"],
        "source": "GitHub REST API v3, public repository metadata only",
        "queries": QUERIES,
        "groups": {name: {"min_stars": floor, "queries": qs}
                   for name, floor, qs in GROUPS},
        "count": len(records),
        "repositories": records,
    }

    # One record per line. Still a single valid JSON document, but git can diff
    # it line by line — a 10 MB file rewritten every day for a year is only
    # cheap if yesterday's version is mostly still there.
    head = {k: v for k, v in index.items() if k != "repositories"}
    body = ",\n  ".join(json.dumps(r, ensure_ascii=False, separators=(",", ":"))
                        for r in records)
    meta = json.dumps(head, ensure_ascii=False, indent=1)[1:-1].rstrip()
    (DATA / "servers.json").write_text(
        "{" + meta + ",\n \"repositories\": [\n  " + body + "\n ]\n}\n")
    (DAILY / f"{TODAY}.json").write_text(json.dumps(snapshot, indent=1, ensure_ascii=False) + "\n")

    cols = ["full_name", "group", "url", "stars", "forks", "language", "license",
            "license_state", "status",
            "days_since_push", "pushed_at", "created_at", "archived", "is_fork",
            "first_seen", "description"]
    with (DATA / "servers.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for rec in records:
            writer.writerow(rec)

    hist = DATA / "history.csv"
    hist_cols = ["date", "repositories", "active", "slowing", "stale", "abandoned",
                 "archived", "no_licence", "no_licence_pct", "nonstandard_licence",
                 "abandoned_of_eligible_pct", "arrived", "left", "total_stars"]
    rows = []
    if hist.exists():
        with hist.open(newline="", encoding="utf-8") as handle:
            rows = [r for r in csv.DictReader(handle) if r.get("date") != TODAY]
    rows.append({
        "date": TODAY,
        "repositories": len(records),
        "active": by_status.get("active", 0),
        "slowing": by_status.get("slowing", 0),
        "stale": by_status.get("stale", 0),
        "abandoned": by_status.get("abandoned", 0),
        "archived": by_status.get("archived", 0),
        "no_licence": len(no_licence),
        "no_licence_pct": snapshot["totals"]["no_licence_pct"],
        "nonstandard_licence": len(nonstandard),
        "abandoned_of_eligible_pct": snapshot["totals"]["abandoned_of_eligible_pct"],
        "arrived": len(arrivals),
        "left": len(departures),
        "total_stars": snapshot["totals"]["stars"],
    })
    rows.sort(key=lambda r: r["date"])
    with hist.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=hist_cols)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps(snapshot["totals"], indent=1))
    if errors:
        print(f"{len(errors)} error(s) recorded in the snapshot", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
