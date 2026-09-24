# agent-vitals

**A daily census of the AI agent tooling ecosystem on GitHub — MCP servers, agent
frameworks, skills and the tools around them. Not a list of what exists, but a
measurement of what is still alive.**

Every awesome-list tells you what was published. None of them tell you what has
been touched since. This repository answers three questions every day, from public
GitHub metadata, and keeps the answers as a time series:

1. How much of the ecosystem is still maintained?
2. How much of it carries a licence you could actually use at work?
3. What appeared, and what went quiet, since yesterday?

## Check your own setup

The same questions, asked of the MCP servers you actually run:
[mcp-upkeep](https://github.com/Keremozdemirra/mcp-upkeep) reads your client configs
and reports, for each server, when its repository was last pushed, whether it is
archived or deprecated, what licence it carries and whether it is pinned. As a
Claude Code plugin it asks before Claude adds a server that is archived, abandoned,
deprecated or unlicensed.

```
/plugin marketplace add Keremozdemirra/mcp-upkeep
/plugin install mcp-upkeep@mcp-upkeep
```

or, from a terminal, `uvx mcp-upkeep`.

## 2026-09-24

- **40,128 repositories** across 13 topic queries in 2 tiers: **mcp** (17,795, 2+ stars), **agents** (22,333, 10+ stars).
- **46.6%** pushed in the last 30 days.
- **6,670 (16.6%) have no licence file at all**, which leaves them under exclusive copyright by default: no permission to use, copy or modify them, whatever the README suggests. A further 3,129 (7.8%) carry a licence GitHub cannot map to a standard identifier — those are licensed, just not in a way a procurement review waves through.
- Only 8,209 of these repositories are even a year old. Among those, **29.1% have not been pushed since** — the headline 6.0% across the whole index is an artefact of how young this ecosystem is.
- Churn since the previous run: **+201 new**, **-36 gone**.

### Maintenance status

| Status | Repositories | Share | Meaning |
| --- | ---: | ---: | --- |
| active | 18,701 | 46.6% | pushed within 30 days |
| slowing | 7,874 | 19.6% | 31-90 days |
| stale | 10,524 | 26.2% | 91-365 days |
| abandoned | 2,392 | 6.0% | no push in over a year |
| archived | 637 | 1.6% | archived by its owner |

### Licences

`no licence file` and `licence GitHub cannot identify` are different things and are
counted separately. The second group has a LICENSE file; GitHub simply cannot match
it to a standard identifier.

| Licence | Repositories | Share |
| --- | ---: | ---: |
| MIT | 22,152 | 55.2% |
| no licence file | 6,670 | 16.6% |
| Apache-2.0 | 5,654 | 14.1% |
| licence GitHub cannot identify | 3,129 | 7.8% |
| AGPL-3.0 | 1,098 | 2.7% |
| GPL-3.0 | 609 | 1.5% |
| CC0-1.0 | 165 | 0.4% |
| BSD-3-Clause | 123 | 0.3% |
| MPL-2.0 | 106 | 0.3% |
| MIT-0 | 86 | 0.2% |

### Most-starred, still maintained

Ranked by stars, restricted to repositories pushed within the last 30 days.

| Repository | Stars | Licence | Last push | Description |
| --- | ---: | --- | --- | --- |
| [affaan-m/ECC](https://github.com/affaan-m/ECC) | 266,380 | MIT | 2026-09-22 | The agent harness performance optimization system. Skills, instincts, memory, security, and research-first dev |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 248,535 | MIT | 2026-09-24 | The agent that grows with you |
| [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | 234,704 | MIT | 2026-09-23 | DeepSeek Harness: Everything is a Plugin. |
| [n8n-io/n8n](https://github.com/n8n-io/n8n) | 205,823 | non-standard | 2026-09-24 | Fair-code workflow automation platform with native AI capabilities. Combine visual building with custom code,  |
| [Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | 187,515 | non-standard | 2026-09-24 | AutoGPT is the vision of accessible AI for everyone, to use and to build on. Our mission is to provide the too |
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 184,014 | AGPL-3.0 | 2026-09-24 | The web data API to search, scrape, and interact at scale. 🔥 |
| [anthropics/skills](https://github.com/anthropics/skills) | 177,872 | **no licence file** | 2026-09-22 | Public repository for Agent Skills |
| [Snailclimb/JavaGuide](https://github.com/Snailclimb/JavaGuide) | 158,847 | Apache-2.0 | 2026-09-22 | Java 面试 & 后端通用面试指南，覆盖计算机基础、数据库、分布式、高并发、系统设计与 AI 应用开发 |
| [langgenius/dify](https://github.com/langgenius/dify) | 157,042 | non-standard | 2026-09-24 | Build Agentic workflows, RAG pipelines, with rich AI model and tool support on one collaborative workspace. De |
| [open-webui/open-webui](https://github.com/open-webui/open-webui) | 152,972 | non-standard | 2026-09-24 | User-friendly AI Interface (Supports Ollama, OpenAI API, ...) |
| [langchain-ai/langchain](https://github.com/langchain-ai/langchain) | 146,967 | MIT | 2026-09-24 | The agent engineering platform. |
| [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | 145,228 | MIT | 2026-09-14 | Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote. |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 136,141 | MIT | 2026-09-24 | A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw, Grok Build & Hermes  |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 130,239 | MIT | 2026-09-21 | An AI skill that provides design intelligence for building professional UI/UX across multiple platforms. |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 121,031 | Apache-2.0 | 2026-09-23 | Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphif |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 116,136 | MIT | 2026-09-24 | Agents that use the browser. |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 107,613 | non-standard | 2026-09-24 | 🪨 why use many token when few token do trick. Viral skill + proxy for coding agents that cuts 65% of tokens by |
| [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) | 107,138 | Apache-2.0 | 2026-09-24 | An open-source AI agent that brings the power of Gemini directly into your terminal. |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 98,772 | MIT | 2026-09-23 | Production-grade engineering skills for AI coding agents. |
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | 97,877 | Apache-2.0 | 2026-09-24 | 🎨 Best DeepSeek Harness Design Plugin. The open-source Claude Design alternative. 🖥️ Local-first desktop app.  |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 95,475 | MIT | 2026-09-23 | A collection of MCP servers. |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) | 94,577 | Apache-2.0 | 2026-09-24 | Persistent Context Across Sessions for Every Agent – Captures everything your agent does during sessions, comp |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 91,247 | Apache-2.0 | 2026-09-24 | RAGFlow is a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with  |
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 89,708 | MIT | 2026-09-23 | Taste-Skill - gives your AI good taste. stops the AI from generating boring, generic slop |
| [koala73/worldmonitor](https://github.com/koala73/worldmonitor) | 87,301 | AGPL-3.0 | 2026-09-24 | Real-time global intelligence dashboard. AI-powered news aggregation, geopolitical monitoring, and infrastruct |

### Popular but unmaintained

Over 50 stars, no push in more than a year. These are the entries that stay on
curated lists long after anyone stopped answering issues.

| Repository | Stars | Last push | Days |
| --- | ---: | --- | ---: |
| [TransformerOptimus/SuperAGI](https://github.com/TransformerOptimus/SuperAGI) | 17,690 | 2025-01-22 | 610 |
| [RayVentura/ShortGPT](https://github.com/RayVentura/ShortGPT) | 7,970 | 2025-02-10 | 591 |
| [BrowserMCP/mcp](https://github.com/BrowserMCP/mcp) | 7,127 | 2025-04-24 | 518 |
| [lharries/whatsapp-mcp](https://github.com/lharries/whatsapp-mcp) | 6,310 | 2025-07-13 | 438 |
| [aiwaves-cn/agents](https://github.com/aiwaves-cn/agents) | 5,967 | 2024-09-26 | 728 |
| [liaokongVFX/MCP-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/MCP-Chinese-Getting-Started-Guide) | 3,573 | 2025-04-23 | 519 |
| [flydelabs/flyde](https://github.com/flydelabs/flyde) | 3,506 | 2025-07-27 | 424 |
| [BAAI-Agents/Cradle](https://github.com/BAAI-Agents/Cradle) | 2,587 | 2024-11-07 | 686 |
| [semanser/codel](https://github.com/semanser/codel) | 2,475 | 2024-04-29 | 878 |
| [dot-agent/nextpy](https://github.com/dot-agent/nextpy) | 2,348 | 2024-05-01 | 876 |
| [trypromptly/LLMStack](https://github.com/trypromptly/LLMStack) | 2,309 | 2024-12-11 | 652 |
| [cjo4m06/mcp-shrimp-task-manager](https://github.com/cjo4m06/mcp-shrimp-task-manager) | 2,150 | 2025-08-21 | 399 |
| [chatmcp/mcpso](https://github.com/chatmcp/mcpso) | 2,107 | 2025-03-26 | 547 |
| [chongdashu/unreal-mcp](https://github.com/chongdashu/unreal-mcp) | 2,085 | 2025-04-22 | 520 |
| [SqueezeAILab/LLMCompiler](https://github.com/SqueezeAILab/LLMCompiler) | 1,886 | 2024-07-10 | 806 |
| [lst97/claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents) | 1,688 | 2025-08-15 | 405 |
| [TIGER-AI-Lab/TheoremExplainAgent](https://github.com/TIGER-AI-Lab/TheoremExplainAgent) | 1,504 | 2025-07-27 | 424 |
| [agi-inc/agent-protocol](https://github.com/agi-inc/agent-protocol) | 1,455 | 2025-04-08 | 534 |
| [gyoridavid/short-video-maker](https://github.com/gyoridavid/short-video-maker) | 1,372 | 2025-06-21 | 460 |
| [browserable/browserable](https://github.com/browserable/browserable) | 1,207 | 2025-08-27 | 393 |

### Quiet, permissive, still asked about

No push in over a year, or archived, yet 200 or more stars, a permissive licence and
five or more open issues. People still arrive; nobody answers. Each is forkable as it
stands. A date, a star count and a licence field, never a verdict on the work.

| Repository | Stars | Open issues | Licence | Last push |
| --- | ---: | ---: | --- | --- |
| [TransformerOptimus/SuperAGI](https://github.com/TransformerOptimus/SuperAGI) | 17,690 | 264 | MIT | 2025-01-22 |
| [bytebot-ai/bytebot](https://github.com/bytebot-ai/bytebot) | 11,085 | 72 | Apache-2.0 | 2025-09-12 |
| [RayVentura/ShortGPT](https://github.com/RayVentura/ShortGPT) | 7,970 | 86 | MIT | 2025-02-10 |
| [BrowserMCP/mcp](https://github.com/BrowserMCP/mcp) | 7,127 | 150 | Apache-2.0 | 2025-04-24 |
| [airweave-ai/airweave](https://github.com/airweave-ai/airweave) | 6,563 | 105 | MIT | 2026-06-05 |
| [lharries/whatsapp-mcp](https://github.com/lharries/whatsapp-mcp) | 6,310 | 248 | MIT | 2025-07-13 |
| [microsoft/TaskWeaver](https://github.com/microsoft/TaskWeaver) | 6,171 | 53 | MIT | 2026-03-23 |
| [aiwaves-cn/agents](https://github.com/aiwaves-cn/agents) | 5,967 | 50 | Apache-2.0 | 2024-09-26 |
| [SolaceLabs/solace-agent-mesh](https://github.com/SolaceLabs/solace-agent-mesh) | 4,925 | 99 | Apache-2.0 | 2026-09-13 |
| [abhi1693/openclaw-mission-control](https://github.com/abhi1693/openclaw-mission-control) | 4,106 | 85 | MIT | 2026-08-06 |
| [browserbase/mcp-server-browserbase](https://github.com/browserbase/mcp-server-browserbase) | 3,413 | 52 | Apache-2.0 | 2026-07-20 |
| [BAAI-Agents/Cradle](https://github.com/BAAI-Agents/Cradle) | 2,587 | 23 | MIT | 2024-11-07 |
| [lmnr-ai/index](https://github.com/lmnr-ai/index) | 2,444 | 6 | Apache-2.0 | 2025-06-09 |
| [dot-agent/nextpy](https://github.com/dot-agent/nextpy) | 2,348 | 23 | Apache-2.0 | 2024-05-01 |
| [Mintplex-Labs/vector-admin](https://github.com/Mintplex-Labs/vector-admin) | 2,242 | 43 | MIT | 2025-04-15 |
| [cjo4m06/mcp-shrimp-task-manager](https://github.com/cjo4m06/mcp-shrimp-task-manager) | 2,150 | 46 | MIT | 2025-08-21 |
| [chatmcp/mcpso](https://github.com/chatmcp/mcpso) | 2,107 | 3,207 | Apache-2.0 | 2025-03-26 |
| [SqueezeAILab/LLMCompiler](https://github.com/SqueezeAILab/LLMCompiler) | 1,886 | 7 | MIT | 2024-07-10 |
| [zhu1090093659/deepseek-pp](https://github.com/zhu1090093659/deepseek-pp) | 1,874 | 30 | Apache-2.0 | 2026-08-13 |
| [jina-ai/langchain-serve](https://github.com/jina-ai/langchain-serve) | 1,638 | 15 | Apache-2.0 | 2023-09-20 |

### Busy, permissive, with open work

Pushed in the last 30 days, 1,000 or more stars, a permissive licence and thirty or more
open issues: maintained, wanted, and short of hands. Ranked by open issues.

| Repository | Open issues | Stars | Licence | Last push |
| --- | ---: | ---: | --- | --- |
| [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | 44,180 | 248,535 | MIT | 2026-09-24 |
| [stablyai/orca](https://github.com/stablyai/orca) | 6,690 | 76,936 | MIT | 2026-09-24 |
| [Osmantic/ODS](https://github.com/Osmantic/ODS) | 3,716 | 6,782 | Apache-2.0 | 2026-09-24 |
| [can1357/oh-my-pi](https://github.com/can1357/oh-my-pi) | 3,139 | 33,092 | MIT | 2026-09-24 |
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 2,877 | 136,141 | MIT | 2026-09-24 |
| [agentuniverse-ai/agentUniverse](https://github.com/agentuniverse-ai/agentUniverse) | 2,539 | 2,366 | Apache-2.0 | 2026-09-14 |
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | 2,292 | 95,475 | MIT | 2026-09-23 |
| [decolua/9router](https://github.com/decolua/9router) | 2,219 | 29,714 | MIT | 2026-09-23 |
| [kirodotdev/KiroCrew](https://github.com/kirodotdev/KiroCrew) | 2,058 | 4,122 | Apache-2.0 | 2026-09-24 |
| [esengine/DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) | 1,908 | 35,699 | MIT | 2026-09-24 |
| [t8y2/dbx](https://github.com/t8y2/dbx) | 1,645 | 20,599 | Apache-2.0 | 2026-09-24 |
| [agno-agi/agno](https://github.com/agno-agi/agno) | 1,613 | 42,328 | Apache-2.0 | 2026-09-24 |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | 1,574 | 81,613 | Apache-2.0 | 2026-09-24 |
| [makecindy/cindy](https://github.com/makecindy/cindy) | 1,538 | 2,812 | Apache-2.0 | 2026-09-24 |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | 1,496 | 91,247 | Apache-2.0 | 2026-09-24 |
| [QwenLM/qwen-code](https://github.com/QwenLM/qwen-code) | 1,474 | 28,108 | Apache-2.0 | 2026-09-24 |
| [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | 1,454 | 121,031 | Apache-2.0 | 2026-09-23 |
| [omnigent-ai/omnigent](https://github.com/omnigent-ai/omnigent) | 1,452 | 10,200 | Apache-2.0 | 2026-09-24 |
| [aden-hive/hive](https://github.com/aden-hive/hive) | 1,355 | 11,071 | Apache-2.0 | 2026-09-14 |
| [gastownhall/beads](https://github.com/gastownhall/beads) | 1,291 | 27,394 | MIT | 2026-09-24 |

### Trend

| Date | Repositories | Active | Abandoned | No licence file | New |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2026-09-11 | 37,950 | 18,134 | 2,285 | 6,454 | +242 |
| 2026-09-12 | 38,067 | 18,123 | 2,288 | 6,466 | +155 |
| 2026-09-13 | 38,259 | 18,173 | 2,297 | 6,502 | +230 |
| 2026-09-14 | 38,414 | 18,181 | 2,307 | 6,538 | +175 |
| 2026-09-15 | 38,664 | 18,365 | 2,315 | 6,582 | +289 |
| 2026-09-16 | 38,783 | 18,389 | 2,328 | 6,585 | +200 |
| 2026-09-17 | 38,953 | 18,460 | 2,335 | 6,594 | +212 |
| 2026-09-18 | 39,135 | 18,482 | 2,350 | 6,609 | +221 |
| 2026-09-19 | 39,257 | 18,537 | 2,355 | 6,623 | +162 |
| 2026-09-20 | 39,418 | 18,564 | 2,362 | 6,637 | +191 |
| 2026-09-21 | 39,627 | 18,641 | 2,370 | 6,643 | +251 |
| 2026-09-22 | 39,750 | 18,643 | 2,376 | 6,650 | +141 |
| 2026-09-23 | 39,963 | 18,736 | 2,385 | 6,664 | +253 |
| 2026-09-24 | 40,128 | 18,701 | 2,392 | 6,670 | +201 |

## Ask it from an agent

The census is an MCP server too, standard library only, four tools: `lookup` a
repository's status and licence, `search` by words with status and licence
filters, `summary` of the latest run, and the two `candidates` lists.

```bash
git clone https://github.com/Keremozdemirra/agent-vitals && cd agent-vitals
claude mcp add agent-vitals -- python3 "$PWD/mcp_server.py"
```

`AGENT_VITALS_REMOTE=1` reads the published index instead of the checkout, so
the clone can stay old. Nothing is written or executed; it answers from
`data/servers.json`.

## Use the data

```bash
curl -sL https://raw.githubusercontent.com/Keremozdemirra/agent-vitals/main/data/servers.csv -o servers.csv
```

| File | What it is |
| --- | --- |
| `data/servers.json` | Full index, one object per repository, with `first_seen` and `status`. |
| `data/servers.csv` | The same index, flat, for spreadsheets and `pandas.read_csv`. |
| `data/history.csv` | One row per day: totals per status, licence counts, churn. |
| `data/daily/YYYY-MM-DD.json` | That day's snapshot, including which repositories arrived and which went quiet. |
| `data/candidates.csv` | The two acted-on lists from the report: `revive` (quiet, permissive, still asked about) and `contribute` (busy, permissive, with open work). |

Everything is committed, so `git log data/history.csv` is the changelog of the
ecosystem itself.

## Method

- Source: the GitHub REST search API, public repository metadata only. Nothing is
  cloned, downloaded or executed.
- Tiers and their star floors:
  - `mcp` — 2+ stars: `topic:mcp-server`, `topic:model-context-protocol`
  - `agents` — 10+ stars: `topic:mcp`, `topic:claude-code`, `topic:ai-agents`, `topic:ai-agent`, `topic:agent-skills`, `topic:agentic-ai`, `topic:claude-skills`, `topic:autonomous-agents`, `topic:llm-agents`, `topic:agent-framework`, `topic:llm-tools`
  The MCP topics name one specific thing, so two stars is enough. The broad agent
  topics are also attached to every tutorial and course repository in the field; ten
  stars is where they start describing tools rather than exercises.
- Each query is sliced by star count until every slice fits under GitHub's
  1000-result ceiling, so this is a census rather than a top-1000 sample.
- `status` is derived from `pushed_at` alone. It measures whether a repository is
  being touched, not whether it is good. A finished, correct tool can sit at
  `abandoned` and still work.
- `license_state` is the field that matters. `spdx` means GitHub matched a
  standard licence; `non-standard` means a LICENSE file exists that GitHub reports
  as `NOASSERTION` (n8n's Sustainable Use License, for one); `none` means no
  licence file was detected at all. Only the last of those means "you have no
  permission to use this", and conflating the two would misrepresent projects
  that did license their work.
- A repository leaves the index when it is deleted, renamed, drops below the
  star floor, or has its topic removed. `left_the_index` does not mean `deleted`,
  and this index cannot tell those cases apart.
- Repository descriptions are third-party text. They are stripped of control
  characters, truncated, and escaped at render time.

## What this is not

- **Not a security audit.** Nothing here says a repository is safe or unsafe. The
  fields are dates, counts and licence identifiers — facts from the API, not
  judgements about anyone's code.
- **Not a quality ranking.** Stars measure attention, not merit.
- **Not a recommendation.** Check anything you install yourself.

## What is in here, and whose it is

Nothing in this repository is anyone else's work. No repository is cloned,
downloaded, or copied. Two kinds of thing are published:

1. **Facts from the GitHub API** — name, URL, star and fork counts, creation and
   last-push dates, detected licence identifier, archived flag. Facts about public
   repositories, not expression, and each one links to its source.
2. **The repository's own one-line description**, as its author wrote it, truncated
   and shown next to a link to the original. This is the only third-party text
   here, and it is used the way every package registry and search index uses it.

Everything else — the collector, the renderer, this text, the analysis — was
written for this repository.

## Licence

- **Code** (`collect.py`, `render.py`, the workflow): MIT.
- **The compilation** — the selection, structure and derived fields in `data/`:
  CC0 1.0. Take it, chart it, fork it, no attribution required.
- **The `description` field**: belongs to whoever wrote it, and is reproduced here
  as a short factual descriptor alongside a link to its source. It is not covered
  by the CC0 grant above, and this index makes no claim over it.
- **The indexed repositories themselves**: their authors', under their own
  licences — which is precisely what this index measures.

If you own a repository listed here and want its description dropped from the
index, open an issue and it will be removed from the next run.

---

_Regenerated automatically. Last run: 2026-09-24T08:53:35+00:00 · status: complete._
