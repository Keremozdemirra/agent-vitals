#!/usr/bin/env python3
"""Regenerate README.md and docs/index.html from the collected data.

Every third-party string reaching a template is escaped for its output format
here, at the boundary. Repository descriptions are attacker-controlled text.
"""

from __future__ import annotations

import datetime as dt
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
DAILY = DATA / "daily"

STATUS_LABEL = {
    "active": "pushed within 30 days",
    "slowing": "31-90 days",
    "stale": "91-365 days",
    "abandoned": "no push in over a year",
    "archived": "archived by its owner",
    "unknown": "no push date",
}


def plural(n: int, one: str, many: str) -> str:
    return one if n == 1 else many


def md(text: str) -> str:
    """Escape for a markdown table cell."""
    return (text.replace("\\", "\\\\").replace("|", "\\|")
                .replace("`", "'").replace("<", "&lt;").replace(">", "&gt;"))


def load() -> tuple[dict, dict, list[dict]]:
    index = json.loads((DATA / "servers.json").read_text())
    snaps = sorted(DAILY.glob("*.json"))
    today = json.loads(snaps[-1].read_text())
    history = []
    hist = DATA / "history.csv"
    if hist.exists():
        import csv
        with hist.open(newline="", encoding="utf-8") as handle:
            history = list(csv.DictReader(handle))
    return index, today, history


def top(records: list[dict], n: int, **filters) -> list[dict]:
    out = [r for r in records if all(r.get(k) == v for k, v in filters.items())]
    out.sort(key=lambda r: -r["stars"])
    return out[:n]


def render_readme(index: dict, today: dict, history: list[dict]) -> str:
    recs = index["repositories"]
    t = today["totals"]
    by = today["by_status"]
    date = today["date"]

    lines = [
        "# agent-vitals",
        "",
        "**A daily census of the AI agent tooling ecosystem on GitHub — MCP servers, agent",
        "frameworks, skills and the tools around them. Not a list of what exists, but a",
        "measurement of what is still alive.**",
        "",
        "Every awesome-list tells you what was published. None of them tell you what has",
        "been touched since. This repository answers three questions every day, from public",
        "GitHub metadata, and keeps the answers as a time series:",
        "",
        "1. How much of the ecosystem is still maintained?",
        "2. How much of it carries a licence you could actually use at work?",
        "3. What appeared, and what went quiet, since yesterday?",
        "",
        f"## {date}",
        "",
        f"- **{t['repositories']:,} repositories** across "
        f"{len(index['queries'])} topic {plural(len(index['queries']), 'query', 'queries')} in "
        f"{len(index.get('groups', {}))} tiers: "
        + ", ".join(f"**{n}** ({c:,}, {index['groups'][n]['min_stars']}+ stars)"
                    for n, c in today.get("by_group", {}).items()) + ".",
        f"- **{t['active_pct']}%** pushed in the last 30 days.",
        f"- **{t['no_licence']:,} ({t['no_licence_pct']}%) have no licence file at all**, which leaves them "
        "under exclusive copyright by default: no permission to use, copy or modify them, whatever the "
        "README suggests. A further "
        f"{t['nonstandard_licence']:,} ({t['nonstandard_licence_pct']}%) carry a licence GitHub cannot map "
        "to a standard identifier — those are licensed, just not in a way a procurement review waves through.",
        f"- Only {t['old_enough_to_be_abandoned']:,} of these repositories are even a year old. Among those, "
        f"**{t['abandoned_of_eligible_pct']}% have not been pushed since** — the headline "
        f"{t['abandoned_pct']}% across the whole index is an artefact of how young this ecosystem is.",
        (f"- First run: the whole index is new. Churn against yesterday appears from tomorrow."
         if today["churn"].get("first_run")
         else "- The query set changed today, so the arrivals below are repositories that came "
              "into scope, not repositories that appeared in the world. Churn is comparable "
              "again from the next run."
         if today["churn"].get("scope_changed")
         else f"- Churn since the previous run: **+{today['churn']['arrived_count']} new**, "
              f"**-{today['churn']['left_count']} gone**."),
        "",
        "### Maintenance status",
        "",
        "| Status | Repositories | Share | Meaning |",
        "| --- | ---: | ---: | --- |",
    ]
    total = max(t["repositories"], 1)
    for key in ["active", "slowing", "stale", "abandoned", "archived", "unknown"]:
        if key in by:
            lines.append(f"| {key} | {by[key]:,} | {100*by[key]/total:.1f}% | {STATUS_LABEL[key]} |")

    lines += ["", "### Licences", "",
              "`no licence file` and `licence GitHub cannot identify` are different things and are",
              "counted separately. The second group has a LICENSE file; GitHub simply cannot match",
              "it to a standard identifier.",
              "", "| Licence | Repositories | Share |", "| --- | ---: | ---: |"]
    for name, count in list(today["by_license"].items())[:10]:
        lines.append(f"| {md(name)} | {count:,} | {100*count/total:.1f}% |")

    lines += [
        "",
        "### Most-starred, still maintained",
        "",
        "Ranked by stars, restricted to repositories pushed within the last 30 days.",
        "",
        "| Repository | Stars | Licence | Last push | Description |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for r in top(recs, 25, status="active"):
        lic = r["license"] or ("**no licence file**"
                               if r.get("license_state") == "none"
                               else "non-standard")
        lines.append(
            f"| [{md(r['full_name'])}]({r['url']}) | {r['stars']:,} | {md(lic)} | "
            f"{r['pushed_at']} | {md(r['description'])[:110]} |"
        )

    lines += [
        "",
        "### Popular but unmaintained",
        "",
        "Over 50 stars, no push in more than a year. These are the entries that stay on",
        "curated lists long after anyone stopped answering issues.",
        "",
        "| Repository | Stars | Last push | Days |",
        "| --- | ---: | --- | ---: |",
    ]
    dead = [r for r in recs if r["status"] == "abandoned" and r["stars"] >= 50]
    dead.sort(key=lambda r: -r["stars"])
    for r in dead[:20]:
        lines.append(f"| [{md(r['full_name'])}]({r['url']}) | {r['stars']:,} | {r['pushed_at']} | {r['days_since_push']:,} |")
    if not dead:
        lines.append("| _none in this run_ | | | |")

    if len(history) > 1:
        lines += ["", "### Trend", "",
                  "| Date | Repositories | Active | Abandoned | No licence file | New |",
                  "| --- | ---: | ---: | ---: | ---: | ---: |"]
        for row in history[-14:]:
            lines.append(
                f"| {row['date']} | {int(row['repositories']):,} | {int(row['active']):,} | "
                f"{int(row['abandoned']):,} | {int(row['no_licence']):,} | +{int(row['arrived'])} |"
            )

    lines += [
        "",
        "## Use the data",
        "",
        "```bash",
        "curl -sL https://raw.githubusercontent.com/Keremozdemirra/agent-vitals/main/data/servers.csv -o servers.csv",
        "```",
        "",
        "| File | What it is |",
        "| --- | --- |",
        "| `data/servers.json` | Full index, one object per repository, with `first_seen` and `status`. |",
        "| `data/servers.csv` | The same index, flat, for spreadsheets and `pandas.read_csv`. |",
        "| `data/history.csv` | One row per day: totals per status, licence counts, churn. |",
        "| `data/daily/YYYY-MM-DD.json` | That day's snapshot, including which repositories arrived and which went quiet. |",
        "",
        "Everything is committed, so `git log data/history.csv` is the changelog of the",
        "ecosystem itself.",
        "",
        "## Method",
        "",
        "- Source: the GitHub REST search API, public repository metadata only. Nothing is",
        "  cloned, downloaded or executed.",
        "- Tiers and their star floors:",
    ] + [
        f"  - `{name}` — {cfg['min_stars']}+ stars: "
        + ", ".join(f"`{q}`" for q in cfg["queries"])
        for name, cfg in index.get("groups", {}).items()
    ] + [
        "  The MCP topics name one specific thing, so two stars is enough. The broad agent",
        "  topics are also attached to every tutorial and course repository in the field; ten",
        "  stars is where they start describing tools rather than exercises.",
        "- Each query is sliced by star count until every slice fits under GitHub's",
        "  1000-result ceiling, so this is a census rather than a top-1000 sample.",
        "- `status` is derived from `pushed_at` alone. It measures whether a repository is",
        "  being touched, not whether it is good. A finished, correct tool can sit at",
        "  `abandoned` and still work.",
        "- `license_state` is the field that matters. `spdx` means GitHub matched a",
        "  standard licence; `non-standard` means a LICENSE file exists that GitHub reports",
        "  as `NOASSERTION` (n8n's Sustainable Use License, for one); `none` means no",
        "  licence file was detected at all. Only the last of those means \"you have no",
        "  permission to use this\", and conflating the two would misrepresent projects",
        "  that did license their work.",
        "- A repository leaves the index when it is deleted, renamed, drops below the",
        "  star floor, or has its topic removed. `left_the_index` does not mean `deleted`,",
        "  and this index cannot tell those cases apart.",
        "- Repository descriptions are third-party text. They are stripped of control",
        "  characters, truncated, and escaped at render time.",
        "",
        "## What this is not",
        "",
        "- **Not a security audit.** Nothing here says a repository is safe or unsafe. The",
        "  fields are dates, counts and licence identifiers — facts from the API, not",
        "  judgements about anyone's code.",
        "- **Not a quality ranking.** Stars measure attention, not merit.",
        "- **Not a recommendation.** Check anything you install yourself.",
        "",
        "## What is in here, and whose it is",
        "",
        "Nothing in this repository is anyone else's work. No repository is cloned,",
        "downloaded, or copied. Two kinds of thing are published:",
        "",
        "1. **Facts from the GitHub API** — name, URL, star and fork counts, creation and",
        "   last-push dates, detected licence identifier, archived flag. Facts about public",
        "   repositories, not expression, and each one links to its source.",
        "2. **The repository's own one-line description**, as its author wrote it, truncated",
        "   and shown next to a link to the original. This is the only third-party text",
        "   here, and it is used the way every package registry and search index uses it.",
        "",
        "Everything else — the collector, the renderer, this text, the analysis — was",
        "written for this repository.",
        "",
        "## Licence",
        "",
        "- **Code** (`collect.py`, `render.py`, the workflow): MIT.",
        "- **The compilation** — the selection, structure and derived fields in `data/`:",
        "  CC0 1.0. Take it, chart it, fork it, no attribution required.",
        "- **The `description` field**: belongs to whoever wrote it, and is reproduced here",
        "  as a short factual descriptor alongside a link to its source. It is not covered",
        "  by the CC0 grant above, and this index makes no claim over it.",
        "- **The indexed repositories themselves**: their authors', under their own",
        "  licences — which is precisely what this index measures.",
        "",
        "If you own a repository listed here and want its description dropped from the",
        "index, open an issue and it will be removed from the next run.",
        "",
        "---",
        "",
        f"_Regenerated automatically. Last run: {today['generated_at']} · status: {today['status']}._",
        "",
    ]
    return "\n".join(lines)


def render_html(index: dict, today: dict, history: list[dict]) -> str:
    recs = index["repositories"]
    t = today["totals"]
    by = today["by_status"]
    total = max(t["repositories"], 1)

    def bar(key: str, colour: str) -> str:
        n = by.get(key, 0)
        return (f'<div class="row"><span class="k">{key}</span>'
                f'<span class="track"><i style="width:{100*n/total:.1f}%;background:{colour}"></i></span>'
                f'<span class="v">{n:,}</span></div>')

    rows = "".join(
        f"<tr><td><a href='{html.escape(r['url'])}'>{html.escape(r['full_name'])}</a></td>"
        f"<td class='n'>{r['stars']:,}</td>"
        f"<td>{html.escape(r['license'] or ('no licence file' if r.get('license_state') == 'none' else 'non-standard'))}</td>"
        f"<td>{html.escape(r['pushed_at'])}</td>"
        f"<td class='d'>{html.escape(r['description'][:120])}</td></tr>"
        for r in top(recs, 40, status="active")
    )
    spark = ""
    if len(history) > 1:
        pts = [int(r["repositories"]) for r in history[-30:]]
        lo, hi = min(pts), max(pts)
        span = max(hi - lo, 1)
        coords = " ".join(
            f"{i*(300/max(len(pts)-1,1)):.1f},{40-(v-lo)*36/span:.1f}"
            for i, v in enumerate(pts)
        )
        spark = f'<svg viewBox="0 0 300 44" class="spark"><polyline points="{coords}"/></svg>'

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>agent-vitals — is the AI agent ecosystem alive?</title>
<meta name="description" content="A daily census of the AI agent tooling ecosystem on GitHub: what is maintained, what is abandoned, and what has no licence.">
<style>
:root{{--bg:#fbfaf8;--fg:#1a1a1a;--mut:#6b6b6b;--line:#e3e0da;--acc:#0b6b52}}
@media(prefers-color-scheme:dark){{:root{{--bg:#111312;--fg:#e8e6e1;--mut:#8f8f8b;--line:#282b2a;--acc:#4ec08f}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 ui-serif,Georgia,'Times New Roman',serif;padding:3rem 1.25rem 5rem}}
main{{max-width:52rem;margin:0 auto}}
h1{{font-size:2rem;margin:0 0 .2rem;letter-spacing:-.02em}}
.sub{{color:var(--mut);margin:0 0 2.5rem;font-size:1.05rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin:0 0 2.5rem}}
.cell{{background:var(--bg);padding:1.1rem 1rem}}
.big{{font:600 1.9rem/1 ui-sans-serif,system-ui;letter-spacing:-.03em;display:block;margin-bottom:.3rem}}
.lab{{color:var(--mut);font-size:.8rem;font-family:ui-sans-serif,system-ui;text-transform:uppercase;letter-spacing:.06em}}
h2{{font-size:1.15rem;margin:2.5rem 0 1rem;font-family:ui-sans-serif,system-ui}}
.row{{display:flex;align-items:center;gap:.75rem;margin:.35rem 0;font-family:ui-sans-serif,system-ui;font-size:.85rem}}
.k{{width:5.5rem;color:var(--mut)}}
.track{{flex:1;height:9px;background:var(--line)}}
.track i{{display:block;height:100%}}
.v{{width:4rem;text-align:right;font-variant-numeric:tabular-nums}}
table{{width:100%;border-collapse:collapse;font-family:ui-sans-serif,system-ui;font-size:.83rem}}
th{{text-align:left;color:var(--mut);font-weight:500;border-bottom:1px solid var(--line);padding:.5rem .6rem .5rem 0}}
td{{padding:.5rem .6rem .5rem 0;border-bottom:1px solid var(--line);vertical-align:top}}
td.n{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
td.d{{color:var(--mut)}}
a{{color:var(--acc)}}
.spark{{width:100%;max-width:300px;height:44px}}
.spark polyline{{fill:none;stroke:var(--acc);stroke-width:1.5}}
.wrap{{overflow-x:auto}}
footer{{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--line);color:var(--mut);font-size:.85rem;font-family:ui-sans-serif,system-ui}}
</style></head><body><main>
<h1>agent-vitals</h1>
<p class="sub">A daily census of the AI agent tooling ecosystem — MCP servers, frameworks, skills. Not what exists, but what is still alive. {html.escape(today['date'])}.</p>
<div class="grid">
<div class="cell"><span class="big">{t['repositories']:,}</span><span class="lab">repositories</span></div>
<div class="cell"><span class="big">{t['active_pct']}%</span><span class="lab">pushed in 30 days</span></div>
<div class="cell"><span class="big">{t['abandoned_of_eligible_pct']}%</span><span class="lab">of those a year old, quiet since</span></div>
<div class="cell"><span class="big">{t['no_licence_pct']}%</span><span class="lab">no licence file</span></div>
</div>
<h2>Maintenance status</h2>
{bar('active','#2f9e6e')}{bar('slowing','#c8a13a')}{bar('stale','#c87d3a')}{bar('abandoned','#b4483c')}{bar('archived','#7a7a7a')}
{('<h2>Index size, last 30 runs</h2>' + spark) if spark else ''}
<h2>Most-starred, still maintained</h2>
<div class="wrap"><table><thead><tr><th>Repository</th><th class="n">Stars</th><th>Licence</th><th>Last push</th><th>Description</th></tr></thead><tbody>{rows}</tbody></table></div>
<footer>
Source: GitHub REST API, public metadata only — nothing cloned, downloaded or executed.
<code>status</code> is derived from <code>pushed_at</code>: it measures activity, not quality or safety.
Compilation CC0 · code MIT · each description belongs to its author and links to its source ·
<a href="https://github.com/Keremozdemirra/agent-vitals">repository</a>.
Generated {html.escape(today['generated_at'])}.
</footer>
</main></body></html>
"""


def main() -> int:
    index, today, history = load()
    (ROOT / "README.md").write_text(render_readme(index, today, history))
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / "docs" / "index.html").write_text(render_html(index, today, history))
    print(f"rendered README.md and docs/index.html for {today['date']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
